import Pkg
Pkg.add("ITensors")

using ITensors

ITensors.op(::OpName"I", ::SiteType"Qubit") = [
  1 0
  0 1
]

function ITensors.op(::OpName"U1", t::SiteType"Qubit"; λ::Number)
    return op("Rn", t; θ=0, ϕ=0, λ=λ)
end

function ITensors.op(::OpName"U2", t::SiteType"Qubit"; ϕ::Number, λ::Number)
    return op("Rn", t; θ=pi/2, ϕ=ϕ, λ=λ)
end

function ITensors.op(::OpName"U3", t::SiteType"Qubit"; θ::Number, ϕ::Number, λ::Number)
    return op("Rn", t; θ=θ, ϕ=ϕ, λ=λ)
end


function ITensors.op(::OpName"S", ::SiteType"Qubit")
    return [
        1 0
        0 1im
    ]
end

ITensors.op(::OpName"Sdag", ::SiteType"Qubit") = [
    1 0
    0 -1im
]

ITensors.op(::OpName"SqrtXdag", ::SiteType"Qubit") = [
    (1-im)/2 (1+im)/2
    (1+im)/2 (1-im)/2
]
ITensors.op(::OpName"SqrtY", ::SiteType"Qubit") = [
    (1+im)/2 (-1-im)/2
    (1+im)/2 (1+im)/2
]
ITensors.op(::OpName"SqrtYdag", ::SiteType"Qubit") = [
    (1-im)/2 (1-im)/2
    (-1+im)/2 (1-im)/2
]
ITensors.op(::OpName"Tdag", ::SiteType"Qubit") = [
    1 0
    0 1/sqrt(2)-im/sqrt(2)
]



function initState(s, qubits::Integer)
    psi = productMPS(s, ["0" for i in 1:qubits])
    return psi
end

function expectation(psi, op)
    exp = inner(psi', op, psi)
    return exp
end

function add_single_qubit_gate(gate_list::Vector, gate_name::String, target_index::Integer)::Vector
    push!(gate_list, (gate_name, target_index))
    return gate_list
end

function add_two_qubit_gate(gate_list::Vector, gate_name::String, control_index::Integer, target_index::Integer)::Vector
    push!(gate_list, (gate_name, control_index, target_index))
    return gate_list
end

function add_three_qubit_gate(gate_list::Vector, gate_name::String, control_index1::Integer, control_index2::Integer, target_index::Integer)::Vector
    push!(gate_list, (gate_name, control_index1, control_index2, target_index))
    return gate_list
end

function add_single_qubit_rotation_gate(gate_list::Vector, gate_name::String, target_index::Integer, param::Number)::Vector
    if gate_name == "Rx" || gate_name == "Ry"
        push!(gate_list, (gate_name, target_index, (θ=param,)))
    elseif gate_name == "Rz"
        push!(gate_list, (gate_name, target_index, (ϕ=param,)))
    elseif gate_name == "U1"
        push!(gate_list, (gate_name, target_index, (λ=param,)))
    else
        raise("Invalid gate name")
    end
    return gate_list
end
function add_single_qubit_rotation_gate(gate_list::Vector, gate_name::String, target_index::Integer, param1::Number, param2::Number)::Vector
    if gate_name == "U2"
        push!(gate_list, (gate_name, target_index, (ϕ=param1, λ=param2)))
    else
        raise("Invalid gate name")
    end
    return gate_list
end
function add_single_qubit_rotation_gate(gate_list::Vector, gate_name::String, target_index::Integer, param1::Number, param2::Number, param3::Number)::Vector
    if gate_name == "U3"
        push!(gate_list, (gate_name, target_index, (θ=param1, ϕ=param2, λ=param3)))
    else
        raise("Invalid gate name")
    end
    return gate_list
end


function gate_list()
    return []
end

function add_pauli(pauli_gates::Vector, pauli_name::String, target_index::Integer)::Vector
    push!(pauli_gates, pauli_name)
    push!(pauli_gates, target_index)
    return pauli_gates
end

function add_coef_pauli(os, coefficient::Number, pauli_gates)
    os += (coefficient, pauli_gates...)
    return os
end

function add_coef_identity(os, coefficient::Number, s)
    os += (coefficient,[isodd(i) ? "I" : div(i,2) for i in 1:(2* length(s))]...)
    return os
end

function sampling(psi, shots)
    orthogonalize!(psi, 1)
    result = []
    for i in 1:shots
        sampling = sample(psi)
        count = 0
        for i in 1:length(sampling)
            count += (sampling[i] - 1) * 2^(i - 1)
        end
        push!(result, count)
    end
    return result
end
