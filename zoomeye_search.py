import re
import argparse
from zoomeye.sdk import ZoomEye

#   Default values

zm = ZoomEye(api_key='YOUR_API_KEY')

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def search_url(data, out_file):
    for j in data:

        if 'rdns' in j:

            if ".," in j["rdns"]:
                multy_dom = j["rdns"].split(".,")
                for i in multy_dom:
                    if i == "********************":
                        print("[HIDDEN]\t%s" % i)
                        break

                    url = "https://%s" % i
                    print("[OK]\t\t%s" % url)
                    out_file.write("%s\n" % url)
            else:
                if j["rdns"] == "********************":
                    print("[HIDDEN]\t%s" % j["rdns"])
                    break

                url = "https://" + j["rdns"]
                print("[OK]\t\t%s" % url)
                out_file.write("%s\n" % url)
        else:

            print("[NOT FOUND]\tNo find RDNS record")


def search_ip(data, out_file):
    ip_list = zm.dork_filter("ip,port")

    for ip, port in ip_list:
        string_ip_port = "{}:{}".format(ip, port)

        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            print("[OK]\t\t%s" % string_ip_port)
            out_file.write("%s\n" % string_ip_port)

        else:
            print("[NOT FOUND]\t%s" % string_ip_port)


def search_ip_url(data, out_file):
    for j in data:

        # string_ip_port = j['ip'] + ":" + str(j['portinfo']['port'])
        string_ip_port = "{}:{}".format(j['ip'], j['portinfo']['port'])
        if 'rdns' in j:
            if j["rdns"] == "********************":
                print("[HIDDEN]\t%s %s" % (j["rdns"], string_ip_port))
                break

            if ".," in j["rdns"]:
                multy_dom = j["rdns"].split(".,")
                for i in multy_dom:
                    url = "https://" + i
                    print("[OK]\t\t%s%s" % (url, string_ip_port))
                    out_file.write("%s\t%s\n" % (url, string_ip_port))
            else:
                url = "https://" + j["rdns"]
                print("[OK]\t\t%s%s" % (url, string_ip_port))
                out_file.write("%s\t%s\n" % (url, string_ip_port))
        else:

            print("[NOT FOUND]\tNo find RDNS record\t%s" % string_ip_port)
            out_file.write("%s\n" % string_ip_port)


def main_search(file_name, dork, ip_bool, url_bool, page_count):
    out_file = open(file_name, "a")

    if url_bool == False and ip_bool == False:
        print("Error with values")
        print("\t\tURL:%s" % url_bool)
        print("\t\tIP:%s" % ip_bool)

        return False

    for page in range(1, page_count):

        data = zm.dork_search(dork, page=page)
        print("----------------------------------------------\n\t\tPage %d received\n\n"%page)
        if url_bool == True and ip_bool == False:
            search_url(data, out_file)
        elif url_bool == False and ip_bool == True:
            search_ip(data, out_file)
        elif url_bool == True and ip_bool == True:
            search_ip_url(data, out_file)

    out_file.close()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', type=str, dest="file_name", default="output.txt", help="output file")
    parser.add_argument('-d', type=str, dest="dork", required=True,
                        help=('zoomeye dork.\n'
                              'example: zimbra +title:"Zimbra Web Client Sign In" +app:"Zimbra mail" +country:"PL"'))
    parser.add_argument('-p', type=int, dest="page", default=5, help="Count of pages from ZoomEye")
    parser.add_argument('--ip', type=str2bool, default=False, help="output IP:PORT")
    parser.add_argument('--url', type=str2bool, default=True, help="output https://URL")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main_search(args.file_name, args.dork, args.ip, args.url, args.page)
    print("\n\n\t\tFINISHED")
