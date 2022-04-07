from sys import exit
from random import randint
from textwrap import dedent

class Scene:

    def __init__(self):
        self.thief = None

    def enter(self):
        print(f'Player stats - HP: {self.thief.hp}, Inv: {self.thief.inventory}.')

class Engine:

    def __init__(self, scene_map, thief):
        self.scene_map = scene_map
        self.thief = thief

    def play(self):
        current_scene = self.scene_map.opening_scene()
        current_scene.thief = self.thief
        last_scene = self.scene_map.next_scene('finished')

        while current_scene != last_scene:
            next_scene_name, next_scene_thief = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)
            current_scene.thief = next_scene_thief


class Thief:

    def __init__(self, hp=100, inventory=['lockpick', 'sleeping_powder', 'dynamite']):
        self.hp = hp
        self.inventory = inventory


class MainCorridor(Scene):

    def enter(self):
        super().enter()
        print(dedent('''
        You are a thief master hired by some anonymous organization to steal
        a priceless artifact from a rich noble in the capital. The plan is ready,
        knife is sharp, inventory is ready (lockpick, sleeping powder and dynamite)
        and the night has come. Time to do your job!

        You are sneaking into the residence via some open window. It appears that
        you\'ve entered main corridor so you hide yourself behind the wall and observe.
        If you want to find out where the artifact is, you will have to examine the
        sleeping room where the house owner is sleeping. From your hideout you can see
        that the door is guarded.

        What is your action?
        1. Throw your sack with sleeping powder at the guard\'s face (type \'throw\')
        2. Wait until the guards shows you his back, so you can attack (type '\wait\')
        3. Sneak to the guard (type '\sneak\')
        '''))

        action = input('> ')

        if action.lower() == 'throw':
            print(dedent('''
            You throw your magic sleeping powder at the guard and he fall\'s asleep
            immediately. The thing is that he falls on an ancient decorative armor
            that crush into pieces with tremendous noise. The guards from all over the villa
            run to check what is all the fuss about and find you. You are stabbed with their
            swords numerous times.
            '''))
            return 'death', self.thief
        elif action.lower() == 'sneak':
            print(dedent('''
            You keep close to corridor\'s wall and try to sneak to the guard. However the
            guard notices you and you start to fight. The guard cuts you in your arm.
            '''))
            self.thief.hp -= 25
            if self.thief.hp > 0:
                print(dedent('''
                You get hurt, but not dead and manage to silence the guard forever. You sneak
                into the bedroom.
                '''))
                return 'sleeping_room', self.thief
            else:
                print('Your wounds are too heavy and you die!')
                return 'death', self.thief
        elif action.lower() == 'wait':
            print(dedent('''
            You stay in your hideout and wait until the guard protecting the sleeping
            shows you his back so you can sneak behind his back. Finally, the opportunity
            comes and you are able to cut guard\'s throat and enter the sleeping room silently.
            '''))
            return 'sleeping_room', self.thief
        else:
            print('Unknown answer')
            return 'main_corridor', self.thief


class SleepingRoom(Scene):

    def enter(self):
        super().enter()
        print(dedent('''
        You are entering the noble\'s bedroom and you can hear the overwhelming
        snoring all over the room. You have to learn the location of the key to the
        treasury. What is your action?

        1. Wake up the noble and bargain his life for the key (type \'wake\')
        2. Search all the furniture in bedroom. (type \'search\')
        3. Open the window to check if you are safe. (type \'open\')
        '''))

        action = input('> ')

        if action.lower() == 'wake':
            print(dedent('''
            You wake up the noble with a punch a threaten him with your knife
            to tell you where the key to his treasury is. He tries to act like
            a hero, but eventually he gives up and discloses all you need to know.
            You use your sleeping powder to make him asleep again in order not
            to raise the alarm.
             '''))
            self.thief.inventory.remove('sleeping_powder')
            return 'office', self.thief
        elif action.lower() == 'search':
            print(dedent('''
            You search the room in order to find any clue. As you are in hurry,
            you accidentally push the bottle of wine which breaks into pieces on
            the floor. The noble wakes up immediately and grabs his crossbow.
            Before you reach him, he manages to shoot you in the leg.
            '''))
            self.thief.hp -= 40
            if self.thief.hp > 0:
                print(dedent('''
                You remove the arrow and angrily interrogate the noble. He is scarred
                as hell, so you learn all you want immediately. You punch him in the
                face so he falls asleep again.
                '''))
                return 'office', self.thief
            else:
                print('Your wounds are too heavy and you die!')
                return 'death', self.thief
        elif action.lower() == 'open':
            print(dedent('''
            You open the window to check if the house stays unalerted. Suddenly
            you hear some noise behind you. It appears that the noble wasn\'t
            sleeping at all as he pushed you outside the window. You are a deadman!
            '''))
            return 'death', self.thief
        else:
            print('Unknown answer')
            return 'sleeping_room', self.thief


class Office(Scene):

    def enter(self):
        super().enter()
        print(dedent('''After you learn the whereabouts of treasury key, you find
        and enter noble\'s office. You find a proper painting and find out that
        behind it there is safe in the wall. How do you open it?

        1. Search the office in order to find the key (type \'search\')
        2. Use your dinamite to destroy the doors. (type \'blow\')
        3. Use your lockpick to break into the safe (type \'break\')
        '''))

        action = input('> ')

        if action.lower() == 'search':
            print(dedent('''
            You are in the middle of ransacking the office in order to find the
            proper key, when some of the guards enter it as a part of their patrol.
            They notice you at once and kill you before you draw your weapon!
            '''))
            return 'death', self.thief
        elif action.lower() == 'blow':
            print(dedent('''
            You decide to use dynamite in order to destroy the safe. You light
            the fuse and run for cover, but the bomb explodes much too early and
            the shock wave pushes you hard at the wall.
            '''))
            self.thief.inventory.remove('dynamite')
            self.thief.hp -= 40
            if self.thief.hp > 0:
                print(dedent('''
                You manage to get up, collect the key from the safe\'s remainings
                and disapear before the guards arrive.
                '''))
                return 'treasury', self.thief
            else:
                print('Your wounds are too heavy and you die!')
                return 'death', self.thief
        elif action.lower() == 'break':
            print(dedent('''
            You decide to break into the safe using your reliable lockpick. Within
            a few minutes you manage to open the safe and collect the key ends up
            with success, even though the lockpick broke during the burglary.
            '''))
            self.thief.inventory.remove('lockpick')
            return 'treasury', self.thief
        else:
            print('Unknown answer')
            return 'sleeping_room', self.thief


class Treasury(Scene):

    @staticmethod
    def set_number(the_list):
        return int(the_list[-1].split('.')[0])

    def final_options(self):
        inventory = self.thief.inventory
        options = [
        '',
        '1. Wait for better circumstances (type \'wait\')',
        '2. Try to fool the guards (type \'fool\')'
        ]

        if 'sleeping_powder' in inventory and 'lockpick' in inventory:
            num = self.set_number(options) + 1
            option = f'{num}. Anaesthetize guards and open the door with lockpick (type \'sleep\')'
            options.append(option)
        if 'dynamite' in inventory:
            num = self.set_number(options) + 1
            option = f'{num}. Use dynamite to kill the guards and destroy the treasury doors (type \'blow\')'
            options.append(option)
        return '\n'.join(options)

    def enter(self):
        super().enter()
        print(dedent('''
        Time for the final round! You enter the basement where the treasury is
        located. You hide yourself behind the wall as you noticed two guards before
        the treasury doors. How will you try to reach your goal?
        ''' + self.final_options()))

        action = input('> ')
        if action.lower() == 'wait':
            print(dedent('''
            You wait and observe the guards, so you can see a good opportunity to attack.
            In the meantime other guards are alarmed that the intruder has entered the villa.
            You are searched and destroyed!
            '''))
            return 'death', self.thief
        elif action.lower() == 'fool':
            print(dedent('''
            When the guards opened the treasury to patrol it, you fall over an old barrel
            to draw their attention. The guards come closer to check the nuisance,
            so you attack them. After a short fight you manage to kill them, but you
            get hurt yourself as well.
            '''))
            self.thief.hp -= 20
            if self.thief.hp > 0:
                print(dedent('''
                Your wounds are not fatal! You manage to enter the treasury, open the
                chest with a key you obtained in the office and run successfully!
                '''))
                return 'finished', self.thief
            else:
                print('Your wounds are too heavy and you die!')
                return 'death', self.thief
        elif action.lower() == 'sleep':
            print(dedent('''
            You throw your sleeping powder at the guards\' faces and make them
            fall asleep immediately. Then you use your lockpick to open the treasury
            door and open the check with the key you obtained in the office. What an
            elegant way to finish your job!
            '''))
            return 'finished', self.thief
        elif action.lower() == 'blow':
            print(dedent('''
            You light the fuse and throw your dynamite at the guards and Treasury
            doors. The explosion kills the guards, destroy the doors, but damages
            the ceiling as well hurting you very badly.
            '''))
            self.thief.hp -= 90
            if self.thief.hp > 0:
                print(dedent('''
                Your wounds are not fatal suprisingly! You manage to enter the treasury,
                open the chest with a key you obtained in the office and run successfully!
                '''))
                return 'finished', self.thief
            else:
                print('Your wounds are too heavy and you die!')
                return 'death', self.thief



class Death(Scene):

    quips = [
    'You\'re so lame!',
    'My Grandma can do better than you.',
    'Maybe knitting is your thing, then...',
    'This option? Really?',
    'No comment...',
    'Just go and be stupid somewhere else!'
    ]

    def enter(self):
        print(Death.quips[randint(0, len(self.quips)-1)])
        exit(1)


class Finished(Scene):

    def enter(self):
        print('You won!!!!')
        return 'finished'


class Map:

    scenes = {
    'main_corridor': MainCorridor(),
    'sleeping_room': SleepingRoom(),
    'office': Office(),
    'treasury': Treasury(),
    'death': Death(),
    'finished': Finished()
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        the_scene = Map.scenes.get(scene_name)
        return the_scene

    def opening_scene(self):
        return self.next_scene(self.start_scene)

if __name__ == '__main__':
    a_map = Map('main_corridor')
    a_game = Engine(a_map, Thief())
    a_game.play()
