txt_path = "data/instances"
dzn_path = "CP/instances"


for k in range(1, 41):
    output_filename = dzn_path + "/ins-" + str(k) + ".dzn"
    input_filename = txt_path + "/ins-" + str(k) + ".txt"

    with open(input_filename, 'r') as f_in:
        lines = f_in.read().splitlines()

        w = lines[0]
        n = lines[1]

        x = []
        y = []

        for i in range(int(n)):
            split = lines[i + 2].split(' ')
            x.append(int(split[0]))
            y.append(int(split[1]))

        with open(output_filename, 'w+') as f_out:
            f_out.write('w = {};\n'.format(w))
            f_out.write('n = {};\n'.format(n))

            f_out.write('x = {};\n'.format(x))
            f_out.write('y = {};\n'.format(y))
