import fastpdb

in_file = fastpdb.PDBFile.read("1AKI.pdb")
atom_array = in_file.get_structure(model=1)

out_file = fastpdb.PDBFile()
out_file.set_structure(atom_array)
out_file.write("test.pdb")