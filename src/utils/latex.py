from datetime import datetime, timedelta

def export_latex(data):
    max_len = []
    head = """
\\noindent\\resizebox{{\\textwidth}}{{!}}{{
\\begin{{tikzpicture}}[x=.5cm, y=1cm]
\\begin{{ganttchart}}{{1}}{{{}}}
[vgrid, hgrid]{{{}}}
\\gantttitle{{Flexible Job Shop Solution}}{{{}}} \\\\
\\gantttitlelist{{1,...,{}}}{{1}} \\\\
"""
    footer = """
\\end{ganttchart}
\\end{tikzpicture}}\n
    """
    body = ""
    start_time = datetime.now()
    for machine, operations in sorted(data.items()):
        counter = 0
        for op in operations:
            max_len.append(op[1])
            label = "{}".format(op[3])
            start_second = start_time + timedelta(minutes=op[0])
            end_second = start_time + timedelta(minutes=op[1])
            date_str = start_second.strftime('%d.%m.%Y')
            date_end = end_second.strftime('%d.%m.%Y')
            start_str = start_second.strftime('%H:%M:%S')
            end_str = end_second.strftime('%H:%M:%S')
            body += "\\Dganttbar{{{}}}{{{}}}{{{}}} \\\\ \\textit{{(from {}-{} to {}-{})}}".format(machine, label, op[1] - op[0], date_str, start_str, date_end, end_str)
            if counter == (len(operations) - 1):
                body += "\\\\ \n"
            else:
                body += "\n"
            counter += 1

    lenM = max(10, max(max_len))
    print(head.format(lenM, lenM, lenM, lenM))
    print(body)
    print(footer)
