with open(snakemake.output[0], "w") as fh_out:
    fh_out.write(snakemake.__dict__)
    for ele in snakemake.input:
        fh_out.write(ele + "\n")

        fh_out.write("&&\n")
    for ele in snakemake.output:
        fh_out.write(ele + "\n")
