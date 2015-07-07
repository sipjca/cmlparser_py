import sys
import xml.etree.ElementTree as ET
import parse as p
import typeofmolecule as tm
import oplsparse as op
import time
import tester

start = time.time()
twoArg = False
hydrogen = False

if len(sys.argv) > 2:
    print "ran"
    old_stdout = sys.stdout
    log_file = open(sys.argv[2],"w")
    sys.stdout = log_file

if len(sys.argv) == 4:
    if sys.argv[3] == "aa":
        hydrogen = True
        p.hydrogen = True

#get filename from commandline
cmlfile = sys.argv[1]

#begin parsing
tree = ET.parse(cmlfile)
root = tree.getroot()

atomList = root.findall('./atomArray/atom')
bondList = root.findall('./bondArray/bond')

#create a bunch of atom and bond objects
atom = p.create_atomobj(atomList)
bond = p.create_bondobj(bondList)

#print the atom and bond objects
#p.print_atoms(atom)
#p.print_bonds(bond)

#get a list of angles formed by the bonds
for i in range(0,len(atom)):
    p.get_num_bonds(atom[i],bond)
AngleList = p.print_find_angles_new(atom,bond)
#p.print_angles(AngleList)

#get the dihedrals and print them
dihedrals = p.find_dihedrals_new(AngleList)
#p.print_dihedrals(dihedrals)

#get the rings and print them
ring = p.find_ring(dihedrals)
ring = p.clean_rings(ring)
#p.print_ring(ring)

#get the fused rings and print them
#TODO
fused = p.find_fused(ring)
#p.print_fused(fused)

#begin to parse the opls file
opls_file = 'oplsaa.prm.txt'
oplsfile = open(opls_file,'r')
oplslist = oplsfile.readlines()

oplsMatrix = op.splitList(oplslist)
oplsMatrix2 = [x for x in oplsMatrix if x != []]
opls_atom_ids = op.getAtoms(oplsMatrix2)
opls_van = op.getVan(oplsMatrix2)
opls_partial = op.getPartial(oplsMatrix2)
opls_bond = op.getBonds(oplsMatrix2)
opls_angle = op.getAngles(oplsMatrix2)
#opls_dihedrals = op.getDihedrals(oplsMatrix2)

opls_atoms = op.create_opls_atom(opls_atom_ids,opls_van,opls_partial)
#op.print_opls_atoms(opls_atoms)

opls_bonds = op.create_opls_bond(opls_bond)
#op.print_opls_bonds(opls_bonds)

opls_angles = op.create_opls_angle(opls_angle)
#op.print_opls_angles(opls_angles)

#opls_dihedral = op.create_opls_dihedral(opls)

#get opls molecules
for i in range(0,len(atom)):
    tm.get_molecule(atom[i],opls_atoms)

#get opls bonds
for i in range(0,len(bond)):
    if p.find_atom_by_id(bond[i].bond_master).atom_type == "H" or p.find_atom_by_id(bond[i].bond_slave).atom_type == "H":
        continue
    op.get_bond(bond[i],opls_bonds)

#get opls angles
for i in range(0,len(AngleList)):
    op.get_angles(AngleList[i],opls_angles)

#print again to see the opls changes, this time printing the extra info
p.print_atoms(atom,True)
#p.print_bonds(bond,True)
p.print_angles(AngleList,True)

#count the atoms found earlier by get_molecule
#tester.count_atoms(opls_atoms,atom)
num_diff_atoms = tester.count_atom_type(atom)
bond_info = tester.opls_bond_info(bond)
angle_info = tester.opls_angle_info(AngleList)

#print the time it takes to make sure it doesnt take too long
#print("--- %s seconds ---" % (time.time() - start))

def print_lammps():
    print "Created by CMLParser\n"
    print "\t%s atoms" % len(atom)
    print "\t%s bonds" % len(bond)
    print "\t%s angles" % len(AngleList)
    print "\t%s dihedrals" % len(dihedrals)
    print "\t0 impropers\n"
    print "\t%s atom types" % len(num_diff_atoms)
    print "\t%s bond types" % len(bond_info)
    print "\t%s angle types" % len(angle_info)
    print "\t1 dihedral types"
    print "\t0 impoper types\n"
    print "\t0.000000 1011.713454 xlo xhi"
    print "\t0.000000 1011.713454 ylo yhi"
    print "\t0.000000 1011.713454 zlo zhi\n"
    print "Masses\n"
    #TODO USE LOOP TO PRINT MASSES
    print "\t"
    print "Bond Coeffs\n"
    for i in range(0,len(bond_info)):
        print "%s %s %s" % (i+1,bond_info[i][0],bond_info[i][1])
    print ""
    print "Angle Coeffs\n"
    for i in range(0,len(angle_info)):
        print "%s %s %s" % (i+1,angle_info[i][0],angle_info[i][1])
    print ""
    print "Atoms\n"
    for i in range(0,len(atom)):
        print "%s chain? %s %.4f %.4f %.4f" % (atom[i].atom_id.replace('a',''),atom[i].id,float(atom[i].x_pos),float(atom[i].y_pos),float(atom[i].z_pos))
    #???? CORRECT?????
    print ""
    print "Bonds\n"
    for i in range(0,len(bond)):
        master = (bond[i].bond_master).replace('a','')
        slave = (bond[i].bond_slave).replace('a','')
        bond_type = 0
        for j in range(0,len(bond_info)):
            if bond[i].bond_equib_len == bond_info[j][0] and bond[i].bond_force_const == bond_info[j][1]:
                bond_type = j+1
        print "%s %s %s %s" % (i+1,bond_type,master,slave)
    print ""
    print "Angles\n"
    for i in range(0,len(AngleList)):
        master = AngleList[i].Angle_master.replace('a','')
        slave1 = AngleList[i].Angle_slave1.replace('a','')
        slave2 = AngleList[i].Angle_slave2.replace('a','')
        angle_type = 0
        for j in range(0,len(angle_info)):
            if AngleList[i].Angle_equib_len == angle_info[j][0] and AngleList[i].Angle_force_const == angle_info[j][1]:
                angle_type = j+1
        print "%s %s %s %s %s" % (i+1,angle_type,master,slave1,slave2)
    print ""
    print "Dihedrals\n"
    for i in range(1,len(dihedrals)):
        master1 = dihedrals[i].Angle_master1.atom_id.replace('a','')
        master2 = dihedrals[i].Angle_master2.atom_id.replace('a','')
        slave1 = dihedrals[i].Angle_slave1.atom_id.replace('a','')
        slave2 = dihedrals[i].Angle_slave2.atom_id.replace('a','')
        print "%s dihedral_type %s %s %s %s" % (i,master1,master2,slave1,slave2)

print_lammps()

print "-----------------------------------"
print "TO PRINT OTHER DATA UNCOMMENT LINES"
print "-----------------------------------"

if twoArg:
    sys.stdout = old_stdout
    log_file.close()
