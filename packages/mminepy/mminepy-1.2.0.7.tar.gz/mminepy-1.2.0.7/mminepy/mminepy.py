import inspect
# 
global comnum
comnum = 0
global list_name_list
list_name_list = []
global type_list
type_list = []
global check_list
check_list = []
global python_space
python_space = 0
global test_value
test_value = 0
global in1
global pl1
global st1
global al_pl_1
global addition_list
addition_list = []
global howmany
howmany = -1
global python_var
python_var = 0
global n
n = 0
global k
k = 0
global var_list
var_list = []
global check_list_var
check_list_var = 0
global javacode
javacode = ''
class space:
    def forfinish(code):
        global python_space
        global javacode
        global java_space
        global howmany
        global check_list
        if code.__contains__("   "*python_space):
            return code
        else:
            java_space -= 1
            javacode = space.getspace(javacode)
            javacode += "}\n"
            python_space -= 1
            return code
    def getspace(string):
        global java_space
        string += "   "*java_space
        return string
def init():
    file = open("data/src/main/resources/plugin.yml","w")
    file.write("name: minepy\nmain: Main.Main\nversion: 1.0\napi-version: 1.16\ncommands:\n")
    file.close()
    global wr1
    wr1 = World()
    global al_wr_1
    al_wr_1 = ArrayList(world())
    global al_pl_1
    al_pl_1 = ArrayList(player())
    global pl1
    pl1 = Player()
    global in1
    in1 = Integer()
    global st1
    st1 = String()
    global lc1
    lc1 = Location()
    global check_list
    global python_var
    python_var += 1
    check_list.append('init')
def println(message):
    global python_var
    python_var += 1
    check_list.append('sys_activity')
class Integer:
    def __init__(self):
        global check_list
        global python_var
        python_var += 1
        check_list.append("define")
    def toString(self):
        global st1
        return st1
class Player:
    def __init__(self):
        global addition_list
        if not addition_list.__contains__('org.bukkit.entity.Player'):
            addition_list.append('org.bukkit.entity.Player')
        global check_list
        global python_var
        python_var += 1
        check_list.append("define")
    def setHealth(self,value):
        global check_list
        global python_var
        python_var += 1
        check_list.append("activity")
    def getName(self):
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar")
        return st1
    def sendMessage(self,*args):
        global check_list
        global python_var
        python_var += 1
        check_list.append("activity")
    def getLocation(self):
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar")
        return lc1
    def teleport(self,Location):
        global check_list
        global python_var
        python_var += 1
        check_list.append("activity")
    def sendTitle(self,main_,sub,open_time,status,close):
        global check_list
        global python_var
        python_var += 1
        check_list.append("activity")
    def hasPlayedBefore(self):
        pass
    def removePotionEffect(self,effectype,*detail):
        global check_list
        global python_var
        python_var += 1
        check_list.append("activity2")
    def addPotionEffect(self,effectype,second,hard,*detail):
        global check_list
        global python_var
        python_var += 1
        check_list.append("activity2")
    def getName(self):
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar")
        return st1
class ArrayList:
    def __init__(self,typeof):
        global addition_list
        if not addition_list.__contains__('java.util.ArrayList'):
            addition_list.append('java.util.ArrayList')
        global check_list
        global python_var
        python_var += 1
        check_list.append("define")
        self.type = typeof
    def add(self,something):
        global check_list
        global python_var
        python_var += 1
        check_list.append("activity")
class String:
    def __init__(self):
        global check_list
        global python_var
        python_var += 1
        check_list.append("define")
class Event:
    def __init__(self,eventname):
        global check_list
        global python_var
        python_var += 1
        check_list.append("define_python")
    def getPlayer(self):
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar")
        return pl1
class Location:
    def __init__(self):
        global addition_list
        if not addition_list.__contains__('org.bukkit.Location'):
            addition_list.append('org.bukkit.Location')
        global check_list
        global python_var
        python_var += 1
        check_list.append("define")
    def getX(self):
        global type_list
        global check_list
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar2")
        type_list.append("int")
        global in1
        return in1
    def getY(self):
        global type_list
        global check_list
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar2")
        type_list.append("int")
        global in1
        return in1
    def getZ(self):
        global type_list
        global check_list
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar2")
        type_list.append("int")
        global in1
        return in1
class Random:
    def __init__(self):
        global addition_list
        addition_list.append('java.util.Random')
        global check_list
        global python_var
        python_var += 1
        check_list.append("define")
    def nextInt(self,value):
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar")
        return 15
class Bukkit:
    def getPlayers():
        global pl1
        return al_pl_1
    def getWorld():
        global al_wr_1
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar")
        return al_wr_1
class Inventory:
    def __init__(self):
        global check_list
        global python_var
        python_var += 1
        check_list.append("define")
class ItemStack:
    def __init__(self):
        global addition_list
        addition_list.append('org.bukkit.inventory.ItemStack;')
        global check_list
        global python_var
        python_var += 1
        check_list.append("define")
class Command:
    def sender():
        global pl1
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar3")
        return pl1
    def label():
        global st1
        global check_list
        global python_var
        python_var += 1
        check_list.append("setvar3")
        return st1
class World:
    def __init__(self):
        global addition_list
        if not addition_list.__contains__('org.bukkit.World'):
            addition_list.append('org.bukkit.World')
        global check_list
        global python_var
        python_var += 1
        check_list.append("define")
def time(when):
    global n
    n += 1
    if n == 1:
        global check_list
        global python_var
        python_var += 1
        check_list.append("while_time")
        return True
    else:
        n = 0
        return False
def event(when):
    global n
    n += 1
    if n == 1:
        global check_list
        global python_var
        python_var += 1
        check_list.append("while_event")
        return True
    else:
        n = 0
        return False
def when(*test):
    global k
    k += 1
    if k == 1:
        global check_list
        global python_var
        python_var += 1
        check_list.append("if")
        return True
    else:
        k = 0
        return False
def repeat(*var_name):
    if len(var_name) == 1:
        list_name = var_name[0]
        global pl1
        global python_var
        python_var += 1
        check_list.append("for")
        g = []
        g.append(pl1)
        global list_name_list
        list_name_list.append(list_name.type)
        if list_name.type == "player":
            return g
def command(some):
    global n
    n += 1
    if n == 1:
        global check_list
        global python_var
        python_var += 1
        check_list.append("command")
        return True
    else:
        n = 0
        return False       
def tell():
    global check_list
    print(check_list)
    global python_var
    python_var += 1
    check_list.append("tell")
def make():
    global enable_space
    global addition_list
    global python_space
    global java_space
    java_space = 0
    global check_list
    global check_list_var
    global javacode
    global howmany
    global python_var
    python_var += 1
    check_list.append("make")
    while check_list[0] != 'init':
        del check_list[0]
    print(check_list)
    javacode = ''
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    file = open(filename,"r")
    lines = file.readlines()
    for i in range(0,len(lines)):
        code = lines[i]
        code = str(code)
        code = code.replace("when=", "")
        getvalue = distinguish_execution(code)
        if getvalue == True:
            m = check_list[check_list_var]
            if len(check_list) > 1:
                if not check_list[1] == 'make':
                    code = space.forfinish(code)
            if m != 'make' and howmany == 1:
                howmany = 0
                code = space.forfinish(code)
                howmany = 1
            code = code.replace("   ","")
            code = code.replace("\n","")
            if not code.__contains__("("):
                code = code.replace(" ","")
                var_name = code.split("=")[0]
                if not var_list.__contains__(var_name):
                    data = code.split("=")[1]
                    if data.__contains__('"'):
                        javacode = space.getspace(javacode)
                        javacode += 'String '+var_name+";\n"
                    else:
                        javacode = space.getspace(javacode)
                        javacode += 'Integer '+var_name+";\n"
                    var_list.append(var_name)
                javacode = space.getspace(javacode)
                code = code.replace("="," = ")
                javacode += code+";\n"
            else:
                if m == 'init':
                    javacode = space.getspace(javacode)
                    javacode += 'public class Main extends JavaPlugin implements Listener{\n'
                    java_space += 1
                    addition_list.append('org.bukkit.plugin.java.JavaPlugin')
                    addition_list.append('org.bukkit.event.Listener')
                    
                elif m == 'while_time':
                    javacode = space.getspace(javacode)
                    javacode += '@Override\n'
                    javacode = space.getspace(javacode)
                    code = code.replace(" ","")
                    code1 = code.replace('whiletime', '')
                    code1 = code1.replace('(', '')
                    code1 = code1.replace(')','')
                    code1 = code1.replace(':','')
                    code1 = code1.replace('\n','')
                    if code1 == "Enable":

                        javacode += 'public void onEnable(){\n'
                    if code1 == "Disable":
                        javacode += 'public void onDisable(){\n'
                    python_space += 1
                    java_space += 1
                elif m == 'while_event':
                    code = code.replace("   ","")
                    if not javacode.__contains__("Bukkit.getPluginManager().registerEvents(this,this)"):
                        addition_list.append("org.bukkit.Bukkit")
                        r = 2*"   "
                        javacode = javacode.replace('public void onEnable(){\n', 'public void onEnable(){\n'+r+'Bukkit.getPluginManager().registerEvents(this,this);\n')
                    global test_value
                    test_value += 1
                    name = 'test'+str(test_value)
                    javacode += "   "*java_space
                    javacode += "@EventHandler\n"
                    code = code.replace(" ","")
                    code1 = code.replace('(', '')
                    code1 = code1.replace(')','')
                    code1 = code1.replace(':','')
                    code1 = code1.replace('\n','')
                    code1 = code1.replace('whileevent', '')
                    if not addition_list.__contains__('org.bukkit.event.EventHandler'):
                        addition_list.append('org.bukkit.event.EventHandler')
                    if code1.__contains__("Player") and not addition_list.__contains__('org.bukkit.event.player.'+code1):
                        addition_list.append('org.bukkit.event.player.'+code1)
                    elif code1.__contains__("Block") and not addition_list.__contains__('org.bukkit.event.block.'+code1):
                        addition_list.append('org.bukkit.event.block.'+code1)
                    elif code1.__contains__("Entity") and not addition_list.__contains__('org.bukkit.event.entity.'+code1):
                        addition_list.append('org.bukkit.event.entity.'+code1)
                    elif code1 == "ProjectileHitEvent":
                        addition_list.append('org.bukkit.event.entity.'+code1)
                    javacode = space.getspace(javacode)
                    javacode += 'public void '+name+'('+code1+' e'+') {\n'
                    python_space += 1
                    java_space += 1
                elif m == 'define_python':
                    pass
                elif m == 'define':
                    javacode = space.getspace(javacode)
                    code = code.replace(" ","")
                    i_list = code.split("=")
                    variable_name = i_list[0]
                    middle_part = i_list[1].replace("(","")
                    middle_part = middle_part.replace(")","")
                    if middle_part.__contains__("ArrayList"):
                        species = middle_part.replace("ArrayList","")
                        k = str(species[0])
                        species = k.upper() + species[1:len(species)]
                        javacode += 'ArrayList<'+species+'> '+variable_name+';\n'
                    elif middle_part == "Random":
                        javacode += 'Random '+variable_name+' = new Random();\n'
                    else:
                        javacode += middle_part+' '+variable_name+';\n'
                elif m == 'activity':
                    i1 = code.split(".")[0]
                    i2 = i1.replace(" ","")
                    javacode = space.getspace(javacode)
                    code = code.replace(i1,i2)
                    code = code.replace(")",'+"")')
                    javacode += code+';\n'
                #potion들 다루어논것
                elif m == 'activity2':
                    code = code.replace(" ","")
                    code += ';\n'
                    code = code.replace(" ","")
                    if code.__contains__("add"):
                        code = code.replace(");","));")
                        code = code.replace("(Potion","(new PotionEffect(Potion")
                    code = code.replace("()","")
                    r = int(code.split(",")[1])
                    r = r * 20
                    code = code.split(",")[0]+','+str(r)+','+code.split(",")[2]
                    javacode = space.getspace(javacode)
                    javacode += code
                    if not addition_list.__contains__("org.bukkit.potion.PotionEffect"):
                        addition_list.append("org.bukkit.potion.PotionEffect")
                        addition_list.append("org.bukkit.potion.PotionEffectType")
                elif m == 'sys_activity':
                    if code.__contains__("println"):
                        code = code.replace(" ","")
                        code += ');\n'
                        javacode = space.getspace(javacode)
                        code = code.replace("println(","")
                        code = code.replace(");",";")
                        code = code.replace(")",'+"")')
                        javacode += 'System.out.println('+code
                elif m == "setnum":
                    javacode = space.getspace(javacode)
                    code = code.replace(" ","")
                    code = code.replace("="," = ")
                    code = code.replace("(","")
                    code = code.replace(")","")
                    if code.__contains__("add"):
                        code = code.replace("add","")
                        code = code.replace("setvar","")
                        code = code.replace(",","+")
                    elif code.__contains__("subtract") or code.__contains__("minus"):
                        code = code.replace("subtract","")
                        code = code.replace("minus","")
                        code = code.replace("setvar","")
                        code = code.replace(",","-")
                    elif code.__contains__("multiply"):
                        code = code.replace("multiply","")
                        code = code.replace("setvar","")
                        code = code.replace(",","*")
                    elif code.__contains__("divide"):
                        code = code.replace("divide","")
                        code = code.replace("setvar","(int) ")
                        code = code.replace(",","/")
                    else:
                        code = code.replace("setvar","")
                    javacode += code+';\n'
                elif m == "setvar":
                    code = code.replace(" ","")
                    code = code.replace("="," = ")
                    javacode = space.getspace(javacode)
                    javacode += code +';\n'
                elif m == "setvar2":
                    code = code.replace(" ","")
                    javacode = space.getspace(javacode)
                    code = code.replace("=", " = ")
                    i1 = code.split("=")[0]
                    i2 = code.split("=")[1]
                    m = type_list[0]
                    del type_list[0]
                    javacode += i1+'= ('+str(m) +')'+ i2+';\n'
                elif m == "setvar3":
                    code = code.replace(" ","")
                    code = code.replace("=", " = ")
                    if code.__contains__("getPlayers()"):
                        javacode = space.getspace(javacode)
                        code = code.replace("Bukkit","(ArrayList<Player>) Bukkit")
                        code = code.replace("getPlayers","getOnlinePlayers")
                        javacode += code +';\n'
                    else:
                        code = code.replace(" ","")
                        javacode = space.getspace(javacode)
                        code = code.replace("Command.sender()", "(Player) sender")
                        code = code.replace("Command.","")
                        code = code.replace("label()", "Label")
                        code = code.replace("="," = ")
                        javacode += code+';\n'
                elif m == "for":
                    code = code.replace(" ","")
                    javacode = space.getspace(javacode)
                    code = code.replace("for","")
                    code = code.replace("t(","t")
                    code = code.replace("):","")
                    code = code.replace("in"," in")
                    code = code.replace("repeat","")
                    code = code.replace("getPlayers()","getOnlinePlayers()")
                    i1 = code.split(" in")[0]
                    i2 = code.split(" in")[1]
                    i2 = i2.replace("\n","")
                    global list_name_list
                    type_var = list_name_list[0]
                    k = str(type_var[0])
                    type_var = k.upper() + type_var[1:len(type_var)]
                    javacode += "for ("+type_var+" "+i1+":"+i2+"){\n"
                    del list_name_list[0]
                    python_space += 1
                    java_space += 1
                elif m == 'if':
                    code = code.replace(" ","")
                    code = code.replace("when","")
                    code = code.replace("while","if")
                    code = code.replace("not","!")
                    code = code.replace(":","{")
                    code = code.replace("and"," && ")
                    javacode = space.getspace(javacode)
                    javacode += code+'\n'
                    java_space += 1
                    python_space += 1
                elif m == 'command':
                    code = space.forfinish(code)
                    global comnum
                    code = code.replace(" ","")
                    code = code.replace('whilecommand("',"")
                    code = code.replace('"):',"")
                    name = 'onCommand'
                    comnum += 1
                    java_space = 1
                    python_space = 0
                    if not javacode.__contains__('public boolean '+name+'(CommandSender sender, Command cmd, String Label, String[] args) {\n'):
                        javacode += '   '
                        javacode += 'public boolean '+name+'(CommandSender sender, Command cmd, String Label, String[] args) {\n'
                    java_space += 1
                    python_space += 1
                    javacode += '   '*2+'if (Label.equalsIgnoreCase("'+code+'")) {\n'
                    java_space += 1
                    howmany = 1
                    if not addition_list.__contains__("org.bukkit.command.Command"): 
                        addition_list.append("org.bukkit.command.Command")
                        addition_list.append("org.bukkit.command.CommandSender")
                    r = 2*"   "
                    # javacode = javacode.replace('public void onEnable(){\n', 'public void onEnable(){\n'+r+'this.getCommand("'+code+'").setExecutor(this);\n')
                    file = open("data/src/main/resources/plugin.yml","a")
                    file.write('  '+code+':\n')
                    file.close()
                elif m == "make":
                    if howmany == 1:
                        while java_space > 0:
                            if java_space == 2:
                                javacode = space.getspace(javacode)
                                javacode += "return false;\n"
                            java_space -= 1
                            javacode = space.getspace(javacode)
                            javacode += "}\n"
                    else:
                        while java_space > 0:
                            java_space -= 1
                            javacode = space.getspace(javacode)
                            javacode += "}\n"
                del check_list[0]
    if not javacode.__contains__("Location"):
        addition_list.remove("org.bukkit.Location")
    if not javacode.__contains__("Player"):
        addition_list.remove("org.bukkit.entity.Player")
    if not javacode.__contains__("ArrayList"):
        addition_list.remove("java.util.ArrayList")
    if not javacode.__contains__("World"):
        addition_list.remove("org.bukkit.World")
    addition = ""
    for code1 in addition_list:
        addition += 'import '+code1 +';\n'
    file = open("data/src/main/java/Main/Main.java","w")
    last_String = 'package Main;\n\n'+addition+javacode
    file.write(last_String)
def distinguish_execution(code):
    code = str(code)
    if not code.__contains__("import"):
        no_blank_i = code.replace(" ","")
        if not no_blank_i[0] == "#":
            if not code == "tell()":
                if not code == "Enable":
                    if not code == "Disable":
                        return True
    return False
class PotionEffectType:
    def FIRE_RESISTANCE(self):
        return "FIRE_RESISTANCE"
    def GLOWING(self):
        return "GLOWING"
    def SATURATION(self):
        return "SATURATION"
    def DAMAGE_RESISTANCE(self):
        return "effect"
    def DOLPHINS_GRACE(self):
        return "effect"
    def HEAL(self):
        return "effect"
    def FAST_DIGGING(self):
        return "effect"
    def HUNGER(self):
        return "effect"
    def SLOW(self):
        return "effect"
    def JUMP(self):
        return "effect"
    def HERO_OF_THE_VILLAGE(self):
        return "effect"
    def LEVITATION(self):
        return "effect"
    def WEAKNESS(self):
        return "effect"
    def LUCK(self):
        return "effect"
    def JUMP(self):
        return "effect"
def PlayerMoveEvent():
    return "PlayerMoveEvent"
def BlockBreakEvent():
    return "BlockBreakEvent"
def PlayerInteractEvent():
    return "PlayerInteractEvent"
def PlayerJoinEvent():
    return "PlayerJoinEvent"
def PlayerItemHeldEvent():
    return "PlayerItemHeldEvent"
def BlockFertilizeEvent():
    return "BlockFertilizeEvent"
def BlockExplodeEvent():
    return "BlockExplodeEvent"
def BlockCookEvent():
    return "PlayerInteractEvent"
def BlockDropItemEvent():
    return "BlockDropItemEvent"
def BlockRedstoneEvent():
    return "BlockRedstoneEvent"
def EntityDeathEvent():
    return "EntityDeathEvent"
def EntityDropItemEvent():
    return "EntityDropItemEvent"
def EntityPickupItemEvent():
    return "EntityPickupItemEvent"
def EntityTeleportEvent():
    return "EntityTeleportEvent"
def PlayerDeathEvent():
    return "PlayerDeathEvent"
def ProjectileHitEvent():
    return "ProjectileHitEvent"
def player():
    return "player"
def world():
    return "world"
def Enable():
    return "Enable"
def Disable():
    return "Disable"