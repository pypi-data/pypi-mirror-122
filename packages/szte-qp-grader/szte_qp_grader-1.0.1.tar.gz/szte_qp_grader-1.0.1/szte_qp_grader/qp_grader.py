from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Operator, process_fidelity
from qiskit.circuit.library import CCXGate, CXGate
from pymongo import MongoClient
from datetime import datetime



def ex1(name, circuit):
    if not isinstance(circuit, QuantumCircuit):
        print("Failed.  You have to pass me a QuantumCircuit object! 😠")
        quit()

    op_toffoli = Operator(CCXGate())
    op_to_check = Operator(circuit)

    if op_toffoli.equiv(op_to_check):
        ops = circuit.count_ops()
        cx_count = ops.get('cx', 0)
        if cx_count != circuit.num_nonlocal_gates():
            print("Failed. You have to decompose the Toffoli gate, not use it 🙂")
            quit()
        
        
        score = cx_count*9 + sum(ops.values())
        gate_set = ['cx', 'id', 'rz', 'sx', 'x']
        if sum([ops.get(gate, 0) for gate in gate_set]) == sum(ops.values()):
            score -= 20
        db_helper("ex1", name, datetime.now().isoformat(), score)
        print(f"Congrats, you succeded 🥳 🎉 Your score: {score}, number of CNOTs: {cx_count}")
        
    else:
        print("Failed. Your circuit does not match the Toffoli gate 😢")
        quit()


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


n2021f=[-9114323017467248753, -8465098064824856893, -2114890825219675351, -2621846298790254809, 1915196622454963318, 1099561697436631331, -6643451585823568934, 2567915220400842819, -5767366680879902057, -2142776183849481026, -1664480349014178327, -7032673461165835623, 4951954955291411174, 620791263194234167, -4410244909376206728, 6311861359281709741, -8367011182691870179, 8622548392992064482, 1516413628231209021, -6008087260861598410, -227148900171811807, -2307351420043883994, 4009587272840781675]

def db_helper(collection_name, name_str, time, score):
    name = hash(name_str)
    if name not in n2021f:
        print("Please enter your last name properly!")
        quit()
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