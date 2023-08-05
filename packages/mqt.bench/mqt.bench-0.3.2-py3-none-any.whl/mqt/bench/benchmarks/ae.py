# Code from https://qiskit.org/documentation/finance/tutorials/00_amplitude_estimation.html

from __future__ import annotations

from mqt.bench.utils import get_estimation_problem
from qiskit.algorithms import AmplitudeEstimation


def create_circuit(num_qubits: int):
    """Returns a quantum circuit implementing Quantum Amplitude Estimation.

    Keyword arguments:
    num_qubits -- number of qubits of the returned quantum circuit
    """

    ae = AmplitudeEstimation(
        num_eval_qubits=num_qubits - 1,  # -1 because of the to be estimated qubit
    )
    problem = get_estimation_problem()

    qc = ae.construct_circuit(problem)
    qc.name = "ae"
    qc.measure_all()

    return qc
