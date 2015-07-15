class Bond(object):
   bond_type = ""
   bond_equib_len = ""
   bond_force_const = ""
   bond_master = ""
   bond_slave = ""
   opls_bond_num = 0
   print_type = 0

   #constructor
   def __init__(self, bond_type, bond_master, bond_slave):
      self.bond_type = bond_type
      self.bond_master = bond_master
      self.bond_slave = bond_slave

def create_bonds(bond,atom):
    """ Creates the bond objects

        Keyword Arguments:
        atom - A list of atom objects
        bond - A list of bond objects
    """
    bonds = []
    for i in range(0,len(bond)):
        currbond = str(bond[i].attrib).split()
        type = currbond[4].replace('}','').replace("'","")
        master = currbond[1].replace('a','').replace(',','').replace("'","")
        slave = currbond[2].replace('a','').replace(',','').replace("'","")
        bonds.append(Bond(type,master,slave))
    change_id_to_atom(bonds,atom)
    return bonds

def change_id_to_atom(bonds,atoms):
    """ Helper method that matches bond and atom names for ease down the line

        Keyword Arguments:
        bonds - The list of bond objects
        atoms - The list of atom objects
    """
    for i in range(0,len(bonds)):
        newbondmaster = bonds[i].bond_master
        newbondslave = bonds[i].bond_slave
        for j in range(0,len(atoms)):
            if atoms[j].atom_id == newbondmaster:
                bonds[i].bond_master = atoms[j]
            if atoms[j].atom_id == newbondslave:
                bonds[i].bond_slave = atoms[j]

def set_opls(bonds,opls_bonds):
    """ Sets the opls data into the bond object

        Keyword Arguments:
        bonds - The list of bond objects to set opls data into
        opls_bonds - The list of opls data to scan
    """
    for i in range(len(bonds)):
        master = bonds[i].bond_master.opls_bondid
        slave = bonds[i].bond_slave.opls_bondid
        for j in range(len(opls_bonds)):
            if master == opls_bonds[j].opls_master and slave == opls_bonds[j].opls_slave:
                bonds[i].bond_equib_len = opls_bonds[j].el
                bonds[i].bond_force_const = opls_bonds[j].fc
            elif master == opls_bonds[j].opls_slave and slave == opls_bonds[j].opls_master:
                bonds[i].bond_equib_len = opls_bonds[j].el
                bonds[i].bond_force_const = opls_bonds[j].fc

def uniq_types(bond):
    """ Gets the unique type of bonds for lammps output

        Keyword Arguments:
        bonds - The list of bond objects to get unique types from
    """
    uniq = []
    uniqadd = []
    for i in range(len(bond)):
        if [bond[i].bond_equib_len,bond[i].bond_force_const] in uniqadd:
            continue
        if bond[i].bond_equib_len == "":
            continue
        uniq.append(bond[i])
        uniqadd.append([bond[i].bond_equib_len,bond[i].bond_force_const])
    return uniq

def get_type(bond,type):
    """ Gets the type of unique bond it is for lammps output

        Keyword Arguments:
        bond - The list of bond objects
        type - The list of unique types
    """
    for i in range(len(bond)):
        for j in range(len(type)):
            if bond[i].bond_force_const == type[j].bond_force_const and bond[i].bond_equib_len == type[j].bond_equib_len:
                bond[i].print_type = j+1