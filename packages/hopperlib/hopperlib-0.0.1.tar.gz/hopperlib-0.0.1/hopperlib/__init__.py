import devtreeutil, webbrowser, os
### Inefficient Declares ###
class wtf:
    def instructions():
        print("""STEPS:
        
        1) call: <wtf.INEFFICIENCY = True>
        
        2) call: <wtf.UNNEEDED_CODE = True>
        
        3) call: <MAKE_PEOPLE_WANT_TO_DIE = True>
        
        4) set all elements within <wtf.USELESS_ARRAY> to True
        
        5) call: <init()>""")
    INEFFICIENCY = False
    UNNEEDED_CODE = False
    MAKE_PEOPLE_WANT_TO_DIE = False
    USELESS_ARRAY = [False, False, False, False, False, False, False, False, False, False]
    def init(x, y):
        if x != "USELESS_CODE" or y != "USELESS_DEPENDENCIES":
            devtreeutil.output.print.color.text_color.RED('Failed to pass correct parameters: "USELESS_CODE", "USELESS_DEPENDENCIES"')
        elif x == "USELESS_CODE" and y == "USELESS_DEPENDENCIES":
            if wtf.INEFFICIENCY and wtf.UNNEEDED_CODE and wtf.MAKE_PEOPLE_WANT_TO_DIE and wtf.USELESS_ARRAY[0] and wtf.USELESS_ARRAY[1] and wtf.USELESS_ARRAY[2] and wtf.USELESS_ARRAY[3] and wtf.USELESS_ARRAY[4] and wtf.USELESS_ARRAY[5] and wtf.USELESS_ARRAY[6] and wtf.USELESS_ARRAY[7] and wtf.USELESS_ARRAY[8] and wtf.USELESS_ARRAY[9]:
                return True
            else:
                devtreeutil.output.print.color.text_color.RED('Library unsuccessfully configured for use: for help, call <hopperlib.wtf.instructions()>')
                return False
        else:
            devtreeutil.output.print.color.text_color.RED('Unknown exception occurred.')

class google_meet:
    class at_100:
        class does_not_explain_stuff:
            class expects_a_room_of_people_to_figure_out_how_to_code_by_themselves_when_only_one_or_two_people_in_the_room_actually_can:
                class whole_room_cries_internally_and_wants_to_throw_computer_out_of_window:
                    class explains_a_lot_of_useless_code:
                        def actual_code_does_this():
                            if wtf.init("USELESS_CODE", "USELESS_DEPENDENCIES"):
                                print("Hello World!")

class a:
    class b:
        class c:
            class d:
                class e:
                    class f:
                        class g:
                            class h:
                                class i:
                                    class j:
                                        class k:
                                            class l:
                                                class m:
                                                    class n:
                                                        class o:
                                                            class p:
                                                                class q:
                                                                    class r:
                                                                        class s:
                                                                            class t:
                                                                                class u:
                                                                                    class v:
                                                                                        class w:
                                                                                            class x:
                                                                                                class y:
                                                                                                    class z:
                                                                                                        def print_in_most_terrible_and_obscure_way():
                                                                                                            print("abcdefghijklmnopqrstuvwxyz")

class CULT:
    def warship():
        webbrowser.open("https://ae01.alicdn.com/kf/H9407fa5d1f154a1688453a711c61bffcl/3D-Pinch-Ball-Pop-It-Push-Bubble-Fidget-Toys-Adult-Stress-Relief-Squeeze-Balls-Toys-Antistress.jpg")

class hopper:
    def crucify(people:list):
        for _i in people:
            devtreeutil.output.print.color.text_color.GREEN(f"{_i} has successfully been crucified!")
    def hypnosis(person:str, activity:str):
        devtreeutil.output.print.color.text_color.GREEN(f"{person} has successfully been hypnotized to {activity}")
    def start_google_meet(ID:str=""):
        webbrowser.open(f"https://meet.google.com/{ID}")
    def writecode(action:str, count:int, type:str, condition:str, code:str='print("Hello World!")', background:bool=False, directory:str=(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))):
        if str(action).lower() == "create":
            if str(type).lower() == "if statement" or str(type).lower() == "if":
                with open(f'{directory}\hopperlib_create_if.txt', 'w') as notepad:
                    for _i in range(0, int(count)):
                        notepad.write(f"""if {str(condition)}:
    {code}
""")
                    if background == True:
                        os.startfile(f'{directory}\hopperlib_create_if.txt')
            elif str(type).lower() == "while loop" or str(type).lower() == "while":
                with open(f'{directory}\hopperlib_create_while.txt', 'w') as notepad:
                    for _i in range(0, int(count)):
                        notepad.write(f"""while {str(condition)}:
    {code}
""")
                    if background == True:
                        os.startfile(f'{directory}\hopperlib_create_while.txt')
            elif str(type).lower() == "for loop" or str(type).lower() == "for":
                with open(f'{directory}\hopperlib_create_for.txt', 'w') as notepad:
                    for _i in range(0, int(count)):
                        notepad.write(f"""for {str(condition)}:
    {code}
""")
                    if background == True:
                        os.startfile(f'{directory}\hopperlib_create_for.txt')
            else:
                devtreeutil.output.print.color.text_color.RED("""Error: Invalid statement type.

Valid statements:
    - if
    - while
    - for""")