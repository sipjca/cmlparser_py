class Angle(object):
    #Angle_master specifies the master angle. Etc for slaves
    Angle_type = 0
    Angle_equib_len = ""
    Angle_force_const = ""
    Angle_master = ""
    Angle_slave1 = ""
    Angle_slave2 = ""
    print_type = 0

    #constructor
    def __init__(self, Angle_type, Angle_master, Angle_slave1, Angle_slave2):
        self.Angle_type = Angle_type
        self.Angle_master = Angle_master
        self.Angle_slave1 = Angle_slave1
        self.Angle_slave2 = Angle_slave2

def set_numbonds(atom,bond):
    numbonds = 0
    bondedTo = []
    for i in range(0,len(bond)):
        if atom.atom_id == bond[i].bond_master.atom_id or atom.atom_id == bond[i].bond_slave.atom_id:
            if atom.atom_id == bond[i].bond_master.atom_id:
                numbonds += 1
                bondedTo.append(bond[i].bond_slave)
            elif atom.atom_id == bond[i].bond_slave.atom_id:
                numbonds += 1
                bondedTo.append(bond[i].bond_master)
    atom.numbonds = numbonds
    atom.atom_bonds = bondedTo

def create_angles(atom,bond):
    angles = []
    for i in range(0,len(atom)):
        set_numbonds(atom[i],bond)
        if atom[i].numbonds > 1:
            for j in range(0,atom[i].numbonds):
                for k in range(j,atom[i].numbonds):
                    atombonds = atom[i].atom_bonds
                    if atombonds[k] != atombonds[j]:
                        angles.append(Angle(1,atom[i],atombonds[j],atombonds[k]))
    return angles

def set_opls(angles,opls_angles):
    for i in range(len(angles)):
        slaves = [int(angles[i].Angle_slave1.opls_bondid),int(angles[i].Angle_slave2.opls_bondid)]
        slaves.sort()
        master = angles[i].Angle_master.opls_bondid
        slaveS = str(slaves[0])
        slaveB = str(slaves[1])
        for j in range(len(opls_angles)):
            if slaveS == opls_angles[j].opls_slave1 and slaveB == opls_angles[j].opls_slave2 and master == opls_angles[j].opls_master:
                angles[i].Angle_equib_len = opls_angles[j].el
                angles[i].Angle_force_const = opls_angles[j].fc
            if j == len(opls_angles)-1 and angles[i].Angle_equib_len == "":
                for k in range(len(opls_angles)):
                    if master == opls_angles[k].opls_master:
                        angles[i].Angle_equib_len = opls_angles[k].el
                        angles[i].Angle_force_const = opls_angles[k].fc

def uniq_types(angles):
    uniq = []
    uniqadd = []
    for i in range(len(angles)):
        if [angles[i].Angle_equib_len,angles[i].Angle_force_const] in uniqadd:
            continue
        uniqadd.append([angles[i].Angle_equib_len,angles[i].Angle_force_const])
        uniq.append(angles[i])
    return uniq

def get_type(angle,type):
    for i in range(len(angle)):
        for j in range(len(type)):
            if angle[i].Angle_force_const == type[j].Angle_force_const and angle[i].Angle_equib_len == type[j].Angle_equib_len:
                angle[i].print_type = j+1
