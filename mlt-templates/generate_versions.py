import yaml
import sys
import os
from subprocess import check_output, CalledProcessError, Popen, PIPE

def run(command, cwd=None):
    try:
        output = check_output(command, cwd=cwd).decode("utf-8")
    except CalledProcessError as e:
        print(e.output)
        sys.exit(1)
    return output

def main():
    if len(sys.argv) != 2:
        print("Incorrect arguments, Please provide absolute path of mlt template directory")
        sys.exit(1)
    if not os.path.isdir(sys.argv[1]):
        print("{0} is not directory, Please provide mlt template directory".format(sys.argv[1]))
        sys.exit(2)

    mlt_template_dir = sys.argv[1]
    version_dict = dict()
    for filename in sorted(os.listdir(mlt_template_dir)):
        if not os.path.isdir(os.path.join(mlt_template_dir,filename)):
            continue


        sha_dict = dict()
        command = "git rev-list HEAD -- {0}".format(os.path.join(mlt_template_dir,filename))

        # TODO: investigate if this guarantees the order
        output = run(command.split(" "))
        v = len(output.strip().split("\n"))
        for sha in output.strip().split("\n"):
            sha_dict["v{0}".format(v)] = str(sha.strip())
            v = v-1

        version_dict[filename] = sha_dict


    with open(mlt_template_dir +'/template_versions.yml', 'w') as outfile:
        yaml.dump(version_dict, outfile, default_flow_style=False)


if __name__ == "__main__":
    main()
