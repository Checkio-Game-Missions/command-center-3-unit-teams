init_code = """
if not "Connected" in USER_GLOBAL:
    raise NotImplementedError("Where is 'Connected'?")

Connected = USER_GLOBAL['Connected']
"""

PASS_CODE = """
RET['code_result'] = True, "Ok"
"""


def prepare_test(middle_code, test_code, show_code, show_answer):
    if show_code is None:
        show_code = middle_code
    return {"test_code": {"python-3": init_code + middle_code + test_code,
                          "python-27": init_code + middle_code + test_code},
            "show": {"python-3": show_code,
                     "python-27": show_code},
            "answer": show_answer}


TESTS = {
    "1. Init": [
        prepare_test('Connected(({"a", "b"}, {"b", "c"}, {"c", "a"}, {"a", "c"}))\n',
                     PASS_CODE, None, None),
        prepare_test('Connected([{"1", "2"}, {"3", "1"}])\n', PASS_CODE, None, None),
    ],
    "2. Add": [
        prepare_test('con = Connected([{"1", "2"}, {"3", "1"}])\n'
                     'add_result = con.add({"2", "4"})\n',
                     "RET['code_result'] = add_result is True, str(add_result)",
                     'con = Connected([{"1", "2"}, {"3", "1"}])\n'
                     'con.add({"2", "4"})',
                     "True"
        ),
        prepare_test('con = Connected([{"And", "Or"}, {"For", "And"}])\n'
                     'add_result = con.add({"It", "Am"})\n',
                     "RET['code_result'] = add_result is True, str(add_result)",
                     'con = Connected([{"And", "Or"}, {"For", "And"}])\n'
                     'con.add({"It", "Am"})\n',
                     "True"),
        prepare_test('con = Connected([{"And", "Or"}, {"For", "And"}])\n'
                     'add_result = con.add({"Or", "And"})\n',
                     "RET['code_result'] = add_result is False, str(add_result)",
                     'con = Connected([{"And", "Or"}, {"For", "And"}])\n'
                     'con.add({"Or", "And"})\n',
                     "True")
    ],
    "3. Remove": [
        prepare_test('con = Connected([{"1", "2"}, {"3", "1"}])\n'
                     'remove_result = con.remove({"2", "4"})\n',
                     "RET['code_result'] = remove_result is False, str(remove_result)",
                     'con = Connected([{"1", "2"}, {"3", "1"}])\n'
                     'con.remove({"2", "4"})',
                     "False"),
        prepare_test('con = Connected([{"1", "2"}, {"3", "1"}])\n'
                     'remove_result = con.remove({"11", "12"})\n',
                     "RET['code_result'] = remove_result is False, str(remove_result)",
                     'con = Connected([{"1", "2"}, {"3", "1"}])\n'
                     'con.remove({"11", "12"})',
                     "False"),

        prepare_test('con = Connected([{"And", "Or"}, {"For", "And"}])\n'
                     'remove_result = con.remove({"And", "Or"})\n',
                     "RET['code_result'] = remove_result is True, str(remove_result)",
                     'con = Connected([{"And", "Or"}, {"For", "And"}])\n'
                     'con.remove({"And", "Or"})\n',
                     "True"),
    ],
    "4. Names": [
        prepare_test(
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'n = con.names()\n',
            'RET["code_result"] = (n == {"nikola", "sophia", "robot", "pilot", "stephen"}, str(n))',
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot}))\n'
            'con.names()',
            '{"nikola", "sophia", "robot", "pilot", "stephen"}'),
        prepare_test(
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'con.remove({"stephen", "robot"})\n'
            'n = con.names()\n',
            'RET["code_result"] = (n == {"nikola", "sophia", "pilot"}, str(n))',
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot}))\n'
            'con.remove({"stephen", "robot"})\n'
            'con.names()',
            '{"nikola", "sophia", "pilot"}'),

    ],
    "5. Connected": [
        prepare_test(
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'n = con.connected("nikola")\n',
            'RET["code_result"] = (n == {"sophia"}, str(n))',
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'con.connected("nikola")',
            '{"sophia"}'),
        prepare_test(
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'n = con.connected("sophia")\n',
            'RET["code_result"] = (n == {"nikola", "pilot"}, str(n))',
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'con.connected("sophia")',
            '{"nikola", "pilot"}'),
        prepare_test(
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'n = con.connected("DDD")\n',
            'RET["code_result"] = (n == set(), str(n))',
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'con.connected("DDD")',
            'set()'),
        prepare_test(
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'con.add({"sophia", "stephen"})\n'
            'con.remove({"sophia", "nikola"})\n'
            'n = con.connected("sophia")\n',
            'RET["code_result"] = (n == {"stephen", "pilot"}, str(n))',
            'con = Connected(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'con.add({"sophia", "stephen"})\n'
            'con.remove({"sophia", "nikola"})\n'
            'con.connected("sophia")\n',
            '{"stephen", "pilot"}'),


    ]




    #     prepare_test(test="str(Building(1, 1, 2, 2))",
    #                  answer="Building(1, 1, 2, 2, 10)", ),
    #     prepare_test(test="str(Building(0.2, 1, 2, 2.2, 3.5))",
    #                  answer="Building(0.2, 1, 2, 2.2, 3.5)", ),
    # ],
    # "3. Corners": [
    #     prepare_test(test="Building(1, 1, 2, 2).corners()",
    #                  answer={"south-west": [1, 1], "north-west": [3, 1], "north-east": [3, 3],
    #                          "south-east": [1, 3]}),
    #     prepare_test(test="Building(100.5, 0.5, 24.3, 12.2, 3).corners()",
    #                  answer={"north-east": [112.7, 24.8], "north-west": [112.7, 0.5],
    #                          "south-west": [100.5, 0.5], "south-east": [100.5, 24.8]}),
    # ],
    # "4. Area, Volume": [
    #     prepare_test(test="Building(1, 1, 2, 2, 100).area()",
    #                  answer=4),
    #     prepare_test(test="Building(100, 100, 135.5, 2000.1).area()",
    #                  answer=271013.55),
    #     prepare_test(test="Building(1, 1, 2, 2, 100).volume()",
    #                  answer=400),
    #     prepare_test(test="Building(100, 100, 135.5, 2000.1).volume()",
    #                  answer=2710135.5),
    # ]

}
