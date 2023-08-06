from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Operator, process_fidelity
from qiskit.circuit.library import CCXGate, CXGate
from pymongo import MongoClient
from datetime import datetime
import hashlib


def ex1(name, circuit):
    if not isinstance(circuit, QuantumCircuit):
        print("Failed.  You have to pass me a QuantumCircuit object! 😠")
        return

    op_toffoli = Operator(CCXGate())
    op_to_check = Operator(circuit)

    if op_toffoli.equiv(op_to_check):
        ops = circuit.count_ops()
        cx_count = ops.get('cx', 0)
        if cx_count != circuit.num_nonlocal_gates():
            print("Failed. You have to decompose the Toffoli gate, not use it 🙂")
            return
        
        
        score = cx_count*9 + sum(ops.values())
        gate_set = ['cx', 'id', 'rz', 'sx', 'x']
        if sum([ops.get(gate, 0) for gate in gate_set]) == sum(ops.values()):
            score -= 20
        db_helper("ex1", name, datetime.now().isoformat(), score)
        print(f"Congrats, you succeded 🥳 🎉 Your score: {score}, number of CNOTs: {cx_count}")
        
    else:
        print("Failed. Your circuit does not match the Toffoli gate 😢")
        return


def ex2a(circuit):
    op_toffoli = Operator(CCXGate())
    op_to_check = Operator(circuit)

    if op_toffoli.equiv(op_to_check):
        print("Congrats, you succeded 🥳 🎉")
    else:
        print("Failed. Your circuit does not match the CU operator 😢")

def ex2b(circuit):
    c_checker = QuantumCircuit(3)
    c_checker.cx(0,2)
    op_checker = Operator(c_checker)
    op_to_check = Operator(circuit)

    if op_checker.equiv(op_to_check):
        print("Congrats, you succeded 🥳 🎉")
    else:
        print("Failed. Your circuit does not match the CU2 operator 😢")
    pass

def ex2c(circuit):
    c_checker = QuantumCircuit(3)
    op_checker = Operator(c_checker)
    op_to_check = Operator(circuit)

    if op_checker.equiv(op_to_check):
        print("Congrats, you succeded 🥳 🎉")
    else:
        print("Failed. Your circuit does not match the CU4 operator 😢")


def ex2(name, circuit):
    cqr = QuantumRegister(3, 'control')
    tqr = QuantumRegister(2, 'target')
    cux = QuantumCircuit(cqr, tqr)
    solutions = prep_ex2()
    for i in range(3):
        cux = cux.compose(solutions[i], [cqr[i], tqr[0], tqr[1]])
    
    op_checker = Operator(cux)
    op_to_check = Operator(circuit)

    if op_checker.equiv(op_to_check):
        score = 20
        gate_set =  ['u1', 'u2', 'u3', 'cx', 'id']
        ops = circuit.count_ops()
        text=""
        if sum([ops.get(gate, 0) for gate in gate_set]) == sum(ops.values()):
            score -= 20
            text="You successfully decomposed your circuit to U and CX gates, good job!"
        score += ops.get('cx', 0)
        if ops.get('ccx', 0) != 0:
            score += 10
        db_helper("ex2", name, datetime.now().isoformat(), score)
        print(f"Congrats, you succeded 🥳 🎉 Your score is {score}. {text}")
    else:
        print("Failed. Your circuit does not match the operator 😢")


n2021f=['afea7f8ac398ea4d40c0f7074823294c79e1607a354e13878ba8fbf9e592c2e1', '874dee3c0d2cd9011416078186547321b770d8932ac074334dd20276a19bd451', 'dc6a452fbafc6b95adee5bf2c0611936b903330ec60b3724dbe331dbfe7d8df1', 'b23ffd57279cc0e6c0690f00c07dddb287abe8513b90cbb76f87931398b298b9', 'bd4cad070e1d5015bbf6575fc01469ee3584e1a49de80b2ac4687faed9f52d6f', '6bbbf6ddcf5cfedc8fa65bef02b3549017811a67dede3dd432cb62b1716c634a', 'd05f8db48bf6a0828e22d988eb68c2fceb3ed841590a9699c63ab4847a7e5c09', 'b824c5e80a46c822a94f258cd864d9b1dffb73afd15ceb57a0978d5db16ae2e1', '631dff88c4b030a04782a7558caaa9ff1f0c85ff153452b5cee25bc7d703c578', '98231ca9d5b83665f8a6b741644aa9eabe4d7d7868001823e2eaa40d0ad8a482', '40805c1add449c79bcb208e65d88a84af16fc8e698408ac2f60fcd21aafdff3d', '57cfd81e24aea4d7e04f90533971e92beee4eeca442f38d39605e5c8c4d55aeb', '7bcbdd452774b8825766c3c26959ff850f19e6b5c9572749f740bcfd328e04ad', '6d5d4d45b3d89be98c30c565d71815bf3052725e58a7256104364067a2f587a7', '5f03e3d6504364a88b37d065c9998ac026d2c998a5a73fa7425b7f1a122c8208', 'da69d42eb7692d9db04e8c1578fb81348cfe081d17ea57618148bd1732c473b7', 'f358d66e98034d7b89fcc4809a24d199b0338b644a7fe3ff54829f3768abf2b3', '12c3d61521a3a27711588dd54f60a44d0b58b93e706c6fb3861e6a4f11c541a9', '79b204ec1ececf6a69f068c65eb5ec8823a0b8acb57eaa1c0e2c5714c34f0371', '58f7c4cc05af8397635c196acaa61db897721a55af565d8d7ec7b2f30c1a9170', '2b427550967cac4e5aca76ad74890b6f41c6b54382cc034b1080454ac89f2c3e', '1c7c375e46850f5b61baa69d47a7a635c058a5b99e52e4b8d353fd0985d887f4', '97c8fb74c4e1e8e6ac3b79aa8b01f5f70cd80f72407d87599953aa0893e76ac0']

def db_helper(collection_name, name_str, time, score):
    name = hashlib.sha256(name_str.encode('UTF-8')).hexdigest()
    if name not in n2021f:
        print("Please enter your last name properly!")
        return
    cluster = MongoClient("mongodb+srv://auto:TaMovHp8O8iVOD4r@cluster0.6jl6a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["qp_2021_fall"]
    collection = db[collection_name]
    data = collection.find({"_id":name})
    try: 
        if data.count() == 0:
            collection.insert_one({"_id":name, "time":time, "score":score, "up_count": 0})   
        elif data.count() == 1:
            upload_count = data[0]["up_count"] + 1
            if score <= data[0]["score"]:
                collection.update_one({"_id":name},{"$set":{"time":time, "score":score, "up_count": upload_count}})
            else:
                collection.update_one({"_id":name},{"$set":{"up_count": upload_count}})
    except:
        print("Database connection failed, please try again.")
            

def prep_ex2():
    u = QuantumCircuit(3)
    u2 = QuantumCircuit(3)
    u4 = QuantumCircuit(3)

    u.ccx(0,1,2)
    u.cx(0,1)
    u2.cx(0,2)

    return [u, u2, u4]