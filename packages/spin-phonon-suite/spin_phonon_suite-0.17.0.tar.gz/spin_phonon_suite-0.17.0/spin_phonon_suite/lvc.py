from fractions import Fraction
from functools import lru_cache, partial

import h5py

import numpy as np
from jax import jvp, jit
import jax.numpy as jnp
from jax.scipy.linalg import block_diag

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from hpc_suite.store import Store
from molcas_suite.generate_input import MolcasComm, MolcasInput, Alaska, \
    Mclr, Emil
from molcas_suite.extractor import make_extractor as make_molcas_extractor
import angmom_suite
from angmom_suite.crystal import ProjectModelHamiltonian, \
    MagneticSusceptibility
from angmom_suite.basis import sf2ws, sf2ws_amfi, unitary_transform, \
    from_blocks, dissect_array, extract_blocks, make_angmom_ops_from_mult

ANG2BOHR = 1.88973


class LVC:

    def __init__(self, sf_ener, sf_linear, sf_mult, geom, sf_amfi=None,
                 sf_angm=None, verbose=False):

        # LVC data
        self.sf_ener = sf_ener
        self.sf_linear = sf_linear

        # Spin multiplicities
        self.sf_mult = sf_mult

        self.sf_amfi = sf_amfi
        self.sf_angm = sf_angm

        self.geom = geom

        if verbose:
            self.print_trans_rot_invariance()
            self.print_grad_norm()

    @property
    def natoms(self):
        return self.geom.shape[0]

    @property
    def ground_ener(self):
        return min(map(min, self.sf_ener))

    @property
    def soc_angm(self):
        return sf2ws(self.sf_angm, self.sf_mult)

    @property
    def soc_spin(self):
        spin_mult = \
            [mult for mult, num in self.sf_mult.items() for _ in range(num)]
        return np.array(make_angmom_ops_from_mult(spin_mult)[0:3])

    def print_grad_norm(self):

        num = len(self.sf_mult)
        fig, axes = plt.subplots(nrows=num, ncols=1, squeeze=False)
        fig.set_size_inches(4, num * 4)

        for idx, (mult, lin) in enumerate(zip(self.sf_mult, self.sf_linear)):
            grad_norm = np.linalg.norm(lin, axis=(2, 3))
            axes[idx][0].title.set_text(f"Spin Multiplicity = {mult}")
            mat = axes[idx][0].matshow(grad_norm, norm=LogNorm())
            fig.colorbar(mat)

        plt.savefig("coupling_norm.pdf", dpi=600)

    def print_trans_rot_invariance(self):
        """Evaluates translational and rotational invariance along and around
        all three coordinate axes
        """

        num = len(self.sf_mult)
        fig, axes = plt.subplots(nrows=num, ncols=1, squeeze=False)
        nrm = np.sqrt(self.natoms)

        fig, axes = plt.subplots(nrows=num, ncols=3, squeeze=False)
        fig.set_size_inches(12, num * 4)

        for idx, (mult, lin) in enumerate(zip(self.sf_mult, self.sf_linear)):
            for vdx, (vec, lab) in enumerate(zip(np.identity(3), 'xyz')):
                inv = np.abs(np.einsum('ijkl,l->ij', lin, vec / nrm)) / \
                             np.linalg.norm(lin, axis=(2, 3))
                axes[idx][vdx].title.set_text(
                    f"axis = {lab}, Spin Multiplicity = {mult}")
                mat = axes[idx][vdx].matshow(inv, norm=LogNorm())
            fig.colorbar(mat, ax=axes[idx].tolist())

        plt.savefig("translational_invariance.pdf", dpi=600)

        fig, axes = plt.subplots(nrows=num, ncols=3, squeeze=False)
        fig.set_size_inches(12, num * 4)

        for idx, (mult, lin) in enumerate(zip(self.sf_mult, self.sf_linear)):
            for vdx, (ax, lab) in enumerate(zip(np.identity(3), 'xyz')):
                vec = np.array([np.cross(c, ax) for c in self.geom])
                inv = np.abs(np.einsum('ijkl,kl->ij', lin,
                                       vec / np.linalg.norm(vec))) / \
                    np.linalg.norm(lin, axis=(2, 3))
                axes[idx][vdx].title.set_text(
                    f"axis = {lab}, Spin Multiplicity = {mult}")
                mat = axes[idx][vdx].matshow(inv, norm=LogNorm())
            fig.colorbar(mat, ax=axes[idx].tolist())

        plt.savefig("rotational_invariance.pdf", dpi=600)

    def to_file(self, f_lvc):

        with h5py.File(f_lvc, 'w') as h:

            # LVC data
            for mult, ener in zip(self.sf_mult, self.sf_ener):
                h.create_dataset(f'{mult}/sf_ener', data=ener)

            for mult, lin in zip(self.sf_mult, self.sf_linear):
                h.create_dataset(f'{mult}/sf_linear', data=lin)

            # coordinates
            h.create_dataset('geom', data=self.geom)

            # spin multiplicities
            h.create_dataset('sf_mult', data=list(self.sf_mult.keys()))
            h.create_dataset('sf_nroots', data=list(self.sf_mult.values()))

            if self.sf_amfi is not None:
                for mult1, row in zip(self.sf_mult, self.sf_amfi):
                    for mult2, amfi in zip(self.sf_mult, row):
                        if abs(mult1 - mult2) <= 1:
                            h.create_dataset(f'{mult1}/{mult2}/sf_amfi',
                                             data=amfi)

            if self.sf_angm is not None:
                for mult, angm in zip(self.sf_mult, self.sf_angm):
                    h.create_dataset(f'{mult}/sf_angm', data=angm)

    @classmethod
    def from_file(cls, f_lvc):

        with h5py.File(f_lvc, 'r') as h:

            # coordinates
            geom = h['geom'][...]

            # Spin multiplicities
            sf_mult = dict(zip(h['sf_mult'][...], h['sf_nroots'][...]))

            # LVC data
            sf_ener = [h[f'{mult}/sf_ener'][...] for mult in sf_mult]
            sf_linear = [h[f'{mult}/sf_linear'][...] for mult in sf_mult]

            try:
                sf_amfi = [[h[f'{mult1}/{mult2}/sf_amfi'][...]
                            if abs(mult1 - mult2) <= 2 else
                            jnp.zeros((3, nroots1, nroots2))
                            for mult1, nroots1 in sf_mult.items()]
                           for mult2, nroots2 in sf_mult.items()]

            except KeyError:
                sf_amfi = None

            try:
                sf_angm = [h[f'{mult}/sf_angm'][...] for mult in sf_mult]
            except KeyError:
                sf_angm = None

        return cls(sf_ener, sf_linear, sf_mult, geom, sf_amfi=sf_amfi,
                   sf_angm=sf_angm)

    @classmethod
    def from_molcas(cls, f_rassi, f_grad_list, verbose=False):
        geom = make_molcas_extractor(
            f_rassi, ("rassi", "center_coordinates"))[()]

        spin_mult = make_molcas_extractor(f_rassi, ("rassi", "spin_mult"))[()]
        sf_mult = dict(zip(*np.unique(spin_mult, return_counts=True)))

        def extract_couplings():
            for grad_file in f_grad_list:

                grad = make_molcas_extractor(grad_file, ("gradients", None))

                for (mult, root), val in iter(grad):
                    yield mult, (root - 1, root - 1), val

                nacs = make_molcas_extractor(grad_file, ("nacs", "CI"))

                for (mult, root1, root2), val in iter(nacs):
                    yield mult, (root1 - 1, root2 - 1), val

        def sf_coupling():

            raw_couplings = list(extract_couplings())

            for umult, nroots in sf_mult.items():
                couplings = np.zeros((nroots, nroots) + geom.shape)

                for mult, (root1, root2), val in raw_couplings:
                    if mult == umult:
                        couplings[root1, root2, :] = val
                        if root1 != root2:
                            couplings[root2, root1, :] = val

                yield couplings

        ener = make_molcas_extractor(f_rassi, ("rassi", "SFS_energies"))[()]
        sf_ener = list(dissect_array(ener, spin_mult))

        amfi = make_molcas_extractor(f_rassi, ("rassi", "SFS_AMFIint"))[()]
        sf_amfi = list(map(list, dissect_array(amfi, spin_mult, spin_mult)))

        angm = make_molcas_extractor(f_rassi, ("rassi", "SFS_angmom"))[()]
        sf_angm = list(extract_blocks(angm, spin_mult))

        return cls(sf_ener, list(sf_coupling()), sf_mult, geom,
                   sf_amfi=sf_amfi, sf_angm=sf_angm, verbose=True)

    def subset(self, subset):

        geom = self.geom[subset]
        sf_linear = [lin[: ,: , subset, :] for lin in self.sf_linear]

        return LVC(self.sf_ener, sf_linear, self.sf_mult, geom,
                   sf_amfi=self.sf_amfi, sf_angm=self.sf_angm)

    def diabatic_hamiltonian(self, geom, soc=False):

        distortion = geom - self.geom

        sf_mch = [jnp.diag(ener) + jnp.einsum('ijkl,kl->ij', lin, distortion)
                  for ener, lin in zip(self.sf_ener, self.sf_linear)]

        if soc:
            soc_potential = sf2ws_amfi(self.sf_amfi, self.sf_mult)
            return sf2ws(sf_mch, self.sf_mult) + soc_potential
        else:
            return sf_mch

    def __call__(self, geom, soc=False):

        if soc:
            dia = self.diabatic_hamiltonian(geom, soc=True)
            soc_ener, soc_trafo = jnp.linalg.eigh(dia)

            def trafo(op):
                return unitary_transform(op, soc_trafo)

            return soc_ener, trafo

        else:
            dia = self.diabatic_hamiltonian(geom)
            sf_ener, sf_trafo = zip(*[jnp.linalg.eigh(v) for v in dia])

            def trafo(op, sf=0):
                Umat = sf_trafo if sf else from_blocks(*sf_trafo)
                return unitary_transform(op, Umat, sf=sf)

            return sf_ener, trafo


def make_lvc_evaluator(h_file, select, order=0, geom=None, coords=None,
                       truncate=None):

    lvc = LVC.from_file(h_file)

    item, option_str = select

    resolve_options = {
        "adiabatic_energies": lambda opt: {'soc': opt == "soc", 'truncate': truncate},
        "diabatic_hamiltonian": lambda opt: {'soc': opt == "soc", 'truncate': truncate},
        "proj": lambda opt: angmom_suite.read_args(['proj'] + opt.split()),
        "sus": lambda opt: angmom_suite.read_args(['sus'] + opt.split())
    }[item]

    options = resolve_options(option_str)

    evaluator = {
        "adiabatic_energies": LVCAdiabaticEnergies,
        "diabatic_hamiltonian": LVCDiabaticHamiltonian,
        "proj": LVCModelHamiltonian,
        "sus": LVCMagneticSusceptibility,
    }[item]

    return evaluator(lvc, order, geom=geom, coords=coords, **options)


class LVCData:

    def __init__(self, lvc, order, *args, geom=None, coords=None, **kwargs):
        self.lvc = lvc
        self.order = order
        self.geom = lvc.geom if geom is None else geom
        self.coords = np.identity(3 * lvc.natoms).reshape((-1, lvc.natoms, 3))\
            if coords is None else coords

        super().__init__(*args, **kwargs)

        self.meta['label'] = \
            tuple([f"coord_{i}" for i in range(order)]) + self.meta['label']

    def format_label(self, lab, axes):
        return axes + super().format_label(lab)

    def __iter__(self):

        def recursive_order(x, func, axes=(), order=0):

            if order == self.order:
                yield from map(lambda val, lab: (self.format_label(lab, axes), val), *func(x))

            elif order < self.order:
                first = axes[-1] if len(axes) else 0

                for axis, coord in enumerate(self.coords[first:], start=1):

                    def _func(x):
                        return jvp(func, (x,), (coord,), has_aux=True)[1:3]

                    yield from recursive_order(
                        x, _func, axes=axes + (axis,), order=order + 1)

        yield from recursive_order(self.geom, self.evaluate)


class LVCAdiabaticEnergies(LVCData, Store):
    def __init__(self, *args, soc=False, truncate=None, **kwargs):
        self.soc = soc
        self.truncate = truncate
        description = \
            ' '. join(["SOC" if self.soc else "MCH", "energies",
                       f"truncated to the lowest {self.truncate} states"
                       if self.truncate else ""])

        label = () if self.soc else ("multiplicity",)

        super().__init__(*args, "Energies", description, **kwargs, label=label,
                         units="au")

    def evaluate(self, x):

        if self.truncate is None or not self.soc:
            ener = self.lvc(x, soc=self.soc)[0]
        else:
            ener = self.lvc(x, soc=self.soc)[0][:self.truncate]

        if self.soc:
            return [ener], [()]
        else:
            return ener, map(lambda lab: (lab,), self.lvc.sf_mult)


class LVCDiabaticHamiltonian(LVCData, Store):
    def __init__(self, *args, soc=False, truncate=None, **kwargs):
        self.soc = soc
        self.truncate = truncate
        description = \
            ' '.join(["Diabatic Hamiltonian matrix between the",
                      f"lowest {self.truncate}" if self.truncate else "",
                      "SOC states" if soc else "MCH states"])

        super().__init__(*args, "Diabatic Hamiltonian", description, **kwargs,
                         label=(), units="au")

    def evaluate(self, x):

        if self.truncate is None or not self.soc:
            hamiltonian = self.lvc.diabatic_hamiltonian(x, soc=self.soc)
        else:
            idc = jnp.ix_(jnp.arange(self.truncate), jnp.arange(self.truncate))
            hamiltonian = self.lvc.diabatic_hamiltonian(x, soc=self.soc)[idc]

        if self.soc:
            return [hamiltonian], [()]
        else:
            return hamiltonian, map(lambda lab: (lab,), self.lvc.sf_mult)


class LVCModelHamiltonian(LVCData, ProjectModelHamiltonian):
    def __init__(self, lvc, *args, **kwargs):
        super().__init__(lvc, *args, None, lvc.sf_mult, **kwargs)

    def evaluate(self, x):

        # parse operators in diabatic basis
        ops = {'sf_angm': self.lvc.sf_angm,
               'sf_mch': self.lvc.diabatic_hamiltonian(x, soc=False),
               'sf_amfi': self.lvc.sf_amfi}

        return super().evaluate(**ops)


class LVCMagneticSusceptibility(LVCData, MagneticSusceptibility):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, None, **kwargs)

    def evaluate(self, x):

        # parse operators in diabatic basis

        return super().evaluate(
            hamiltonian=self.lvc.diabatic_hamiltonian(x, soc=True),
            spin=self.lvc.soc_spin,
            angm=self.lvc.soc_angm
        )


def generate_lvc_input(old_path, old_proj, num_root, jobiph_idx,
                       mclr_extra=((), {}), alaska_extra=((), {})):

    # Circular range generator from
    # https://stackoverflow.com/questions/40970290/circular-range-in-python
    def crange(start, end, modulo):
        if start > end:
            while start < modulo:
                yield start
                start += 1
            start = 0

        while start < end:
            yield start
            start += 1

    files = [
        Emil('copy', src, dest) for src, dest in [
            (f"{old_path}/{old_proj}.RunFile", "$Project.RunFile"),
            (f"{old_path}/{old_proj}.OneInt", "$Project.OneInt"),
            (f"{old_path}/{jobiph_idx}_IPH", "$Project.JobIph"),
            (f"{old_path}/{old_proj}.ChDiag", "$Project.ChDiag"),
            (f"{old_path}/{old_proj}.ChMap", "$Project.ChMap"),
            (f"{old_path}/{old_proj}.ChRed", "$Project.ChRed"),
            (f"{old_path}/{old_proj}.ChRst", "$Project.ChRst"),
            (f"{old_path}/{old_proj}.ChVec1", "$Project.ChVec1"),
            (f"{old_path}/{old_proj}.QVec00", "$Project.QVec00")
        ]
    ]

    input_name = r"lvc_root{:0" + str(len(str(num_root))) + r"}.input"

    for iroot in range(1, num_root + 1):

        inp = []

        if num_root % 2 == 0:
            if iroot <= num_root // 2:
                jrange = crange(
                    iroot % num_root,
                    (iroot + num_root // 2) % num_root,
                    num_root
                )

            else:
                jrange = crange(
                    iroot % num_root,
                    (iroot + num_root // 2 - 1) % num_root,
                    num_root
                )
        else:
            jrange = crange(
                iroot % num_root,
                (iroot + num_root // 2) % num_root,
                num_root
            )

        inp.append(MolcasComm('Gradient'))

        inp.append(Mclr(*mclr_extra[0], sala=f"{iroot}", **mclr_extra[1]))

        inp.append(
            Alaska(*alaska_extra[0], root=f"{iroot}", **alaska_extra[1]))

        for jroot in jrange:

            inp.append(MolcasComm('Nonadiabatic coupling'))

            inp.append(
                Mclr(*mclr_extra[0], nac="{} {}".format(iroot, jroot + 1),
                     **mclr_extra[1]))

            inp.append(Alaska(
                *alaska_extra[0],
                nac="{} {}".format(iroot, jroot + 1),
                **alaska_extra[1]))

        MolcasInput(
            *files, *inp,
            title="LVC parametrisation generated by spin-phonon_suite"
        ).write(input_name.format(iroot))
