from PIL import Image, ImageDraw
import sys
import binascii
import hashlib
import subprocess


CATEGORY = 'stegano'
SCORE = 100
NAME = "0xDEAD pixel"

HTML_EN = ''' I have some problems with my LCD, so I can't watch the cartoon. Can you help me? '''
HTML_RU = ''' У меня какие-то проблемы с монитором, поэтому я не могу смотреть любимый мультик. Поможешь? '''


def get_flag(team):
    hash_object = hashlib.md5(team.encode('utf-8'))
    flag = 'RUCTF' + hash_object.hexdigest()[:8]


def generate_video(team, dump_dir):
    string = '0' + bin(int(binascii.hexlify(bytes(get_flag(team), 'utf-8'), 16))[2:]

    string=string.rjust(105, '0')

    for i in range(1, 105):
        img=Image.open('original/image-' + str(i) + '.png')
        draw=ImageDraw.Draw(img)
        draw.point((13, 37),
                   (int(string[i])*255, int(string[i])*255, int(string[i])*255))
        img.save(dump_dir+'/image-' + str(i) + '.png', 'PNG')

    # Video generation: avconv -i "image-%d.png" -r 25 -c:v libx264 -crf 20 -pix_fmt yuv420p video.mov
    # Requirements (apt-packages):
    # libav-tools libavcodec-extra-53 libavdevice-extra-53
    # libavformat-extra-53 libavutil-extra-51 libpostproc-extra-52
    # libswscale-extra-2

    subprocess.call(
        "avconv -i 'image-%d.png' -r 25 -c:v libx264 -crf 20 -pix_fmt yuv420p" + dump_dir + "/static/video_" + team + ".mov")
    return "static/video_" + team + ".mov"

def check_task(team, answer):
    if answer == get_flag(team):
        print("Correct!")
        return True
    else:
        print("Incorrect :(")
        return False

def main():
    action=sys.argv[1].lower()
    if action == 'id':
        print("{}:{}".format(CATEGORY, SCORE))
    elif action == 'series':
        print(CATEGORY)
    elif action == 'name':
        print(NAME)
    elif action == 'create':
        dump_dir=sys.argv[2]
        team_id=sys.argv[3]
        quid=generate_video(team_id)
        if quid is None:
            print("Can't create task")
            exit(1)
        else:
            print("ID:" + str(team_id+'pix'))
            print("html[en]:{}".format(HTML_EN))
            print("html[ru]:{}".format(HTML_RU))
            print("file:{}".format(quid))
    elif action == 'user':
        dump_dir=sys.argv[2]
        quid=sys.argv[3]
        answer=sys.stdin.readline().strip()
        status=check_task(team, answer)
        stat=0 if status else 1
        print("Exiting with " + str(status))
        exit(stat)
    else:
        print("No such action: '{}' available actions are: id, series, name, create, user".format(
            action), file=sys.stderr)
        exit(1)

if __name__ == '__main__':
    main()
