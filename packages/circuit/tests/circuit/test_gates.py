from collections.abc import Mapping
from typing import Callable

import numpy as np

from quri_parts.circuit import (
    CNOT,
    CZ,
    RX,
    RY,
    RZ,
    SWAP,
    U1,
    U2,
    U3,
    H,
    Identity,
    ParametricPauliRotation,
    ParametricQuantumGate,
    ParametricRX,
    ParametricRY,
    ParametricRZ,
    Pauli,
    PauliRotation,
    QuantumCircuit,
    QuantumGate,
    S,
    Sdag,
    SqrtX,
    SqrtXdag,
    SqrtY,
    SqrtYdag,
    T,
    Tdag,
    X,
    Y,
    Z,
    gate_names,
)

_factory_name_map: Mapping[Callable[[int], QuantumGate], str] = {
    Identity: gate_names.Identity,
    X: gate_names.X,
    Y: gate_names.Y,
    Z: gate_names.Z,
    H: gate_names.H,
    S: gate_names.S,
    Sdag: gate_names.Sdag,
    SqrtX: gate_names.SqrtX,
    SqrtXdag: gate_names.SqrtXdag,
    SqrtY: gate_names.SqrtY,
    SqrtYdag: gate_names.SqrtYdag,
    T: gate_names.T,
    Tdag: gate_names.Tdag,
}

_rotation_factory_name_map: Mapping[Callable[[int, float], QuantumGate], str] = {
    RX: gate_names.RX,
    RY: gate_names.RY,
    RZ: gate_names.RZ,
}

_parametric_factory_name_map: Mapping[Callable[[int], ParametricQuantumGate], str] = {
    ParametricRX: gate_names.ParametricRX,
    ParametricRY: gate_names.ParametricRY,
    ParametricRZ: gate_names.ParametricRZ,
}


def test_gate_creation() -> None:
    # Single qubit gate
    for f, name in _factory_name_map.items():
        assert f(5) == QuantumGate(name, target_indices=(5,))

    # Single qubit gate with single parameter
    theta = np.random.rand()
    for rf, name in _rotation_factory_name_map.items():
        assert rf(5, theta) == QuantumGate(name, target_indices=(5,), params=(theta,))

    # U gates
    theta, phi, lmd = np.random.rand(3)
    assert U1(5, lmd) == QuantumGate(gate_names.U1, target_indices=(5,), params=(lmd,))
    assert U2(5, phi, lmd) == QuantumGate(
        gate_names.U2, target_indices=(5,), params=(phi, lmd)
    )
    assert U3(5, theta, phi, lmd) == QuantumGate(
        gate_names.U3, target_indices=(5,), params=(theta, phi, lmd)
    )

    # 2 qubit gates
    assert CNOT(5, 7) == QuantumGate(
        gate_names.CNOT, control_indices=(5,), target_indices=(7,)
    )
    assert CZ(5, 7) == QuantumGate(
        gate_names.CZ, control_indices=(5,), target_indices=(7,)
    )
    assert SWAP(5, 7) == QuantumGate(gate_names.SWAP, target_indices=(5, 7))

    # Pauli gates
    target_indices = (1, 3, 5)
    pauli_ids = (3, 1, 2)
    theta = np.random.rand()
    assert Pauli(target_indices, pauli_ids) == QuantumGate(
        gate_names.Pauli, target_indices=target_indices, pauli_ids=pauli_ids
    )
    assert PauliRotation(target_indices, pauli_ids, theta) == QuantumGate(
        gate_names.PauliRotation,
        target_indices=target_indices,
        pauli_ids=pauli_ids,
        params=(theta,),
    )

    # Parametric gates
    for pf, name in _parametric_factory_name_map.items():
        assert pf(5) == ParametricQuantumGate(name, target_indices=(5,))
    assert ParametricPauliRotation(target_indices, pauli_ids) == ParametricQuantumGate(
        gate_names.ParametricPauliRotation,
        target_indices=target_indices,
        pauli_ids=pauli_ids,
    )


def test_gate_addition() -> None:
    theta, phi, lmd = np.random.rand(3)
    target_indices = (2, 0, 1)
    pauli_ids = (3, 1, 2)

    lc = QuantumCircuit(3)
    gates = [
        Identity(0),
        X(0),
        Y(0),
        Z(0),
        H(0),
        S(0),
        Sdag(0),
        SqrtX(0),
        SqrtXdag(0),
        SqrtY(0),
        SqrtYdag(0),
        T(0),
        Tdag(0),
        RX(0, theta),
        RY(0, theta),
        RZ(0, theta),
        U1(0, lmd),
        U2(0, phi, lmd),
        U3(0, theta, phi, lmd),
        CNOT(0, 1),
        CZ(0, 1),
        SWAP(0, 1),
        Pauli(target_indices, pauli_ids),
        PauliRotation(target_indices, pauli_ids, theta),
    ]
    lc.extend(gates)

    mc = QuantumCircuit(3)
    mc.add_Identity_gate(0)
    mc.add_X_gate(0)
    mc.add_Y_gate(0)
    mc.add_Z_gate(0)
    mc.add_H_gate(0)
    mc.add_S_gate(0)
    mc.add_Sdag_gate(0)
    mc.add_SqrtX_gate(0)
    mc.add_SqrtXdag_gate(0)
    mc.add_SqrtY_gate(0)
    mc.add_SqrtYdag_gate(0)
    mc.add_T_gate(0)
    mc.add_Tdag_gate(0)
    mc.add_RX_gate(0, theta)
    mc.add_RY_gate(0, theta)
    mc.add_RZ_gate(0, theta)
    mc.add_U1_gate(0, lmd)
    mc.add_U2_gate(0, phi, lmd)
    mc.add_U3_gate(0, theta, phi, lmd)
    mc.add_CNOT_gate(0, 1)
    mc.add_CZ_gate(0, 1)
    mc.add_SWAP_gate(0, 1)
    mc.add_Pauli_gate(target_indices, pauli_ids)
    mc.add_PauliRotation_gate(target_indices, pauli_ids, theta)

    assert lc == mc
