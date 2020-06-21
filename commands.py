from emorun.constants import *
cmds = []
import logging
import copy
logger = logging.getLogger()
from telegram import InlineKeyboardButton as Ikb
from telegram import InlineKeyboardMarkup as Ikm


def start(update, context):
    # get or create + logging
    update.message.reply_text(MESSAGES['start'])
start.short = 'Beginne die Unterhaltung'
start.long = 'Beginne die Unterhaltung /start oder durch Drücken des Start-Buttons. Wenn ich dich in Ruhe lassen soll /stop.'
cmds.append(start)


def help(update, context):
    """
    cmds = '\n'
    for cmd in commands:
        name = cmd.name if hasattr(cmd, 'name') else cmd.__name__
        desc = ' - {}'.format(cmd.short) if hasattr(cmd, 'short') else ''
        cmds += '`/'+name+'`' + desc + '\n'
    update.message.reply_text(MESSAGES['help'].format(cmds), parse_mode='Markdown')
    """
    update.message.reply_text(MESSAGES['help'], parse_mode='Markdown')
help.short = 'Hilfe und Befehle anzeigen'
help.long = 'Ich zeige dir wie du mit mir umgehen kannst.'
cmds.append(help)


def stop(update, context):
    update.message.reply_text(MESSAGES['stop'], parse_mode='Markdown')
help.short = 'Verbiete mir in diesen Chat zu schreiben'
help.long = 'Ich werde keine automatischen Nachrichten mehr schicken aber noch auf Befehle reagieren.'
cmds.append(stop)


themes = {
    'default': {
        'g': ''
    }
}


def load_map(update, context, name='first'):
    """ convert map string to 2d-list, set start pos
    """
    map = [[c for c in row] for row in MAPS[name]]
    context.chat_data['map'] = map
    for j, y in enumerate(map):
        for i, x in enumerate(map[j]):
            if x == '0':
                context.chat_data['pos'] = [i, j]
                found = True
                return
    if not found:
        logger.error('No start point (0) found.. map not valid')



def render(update, context):
    frame = copy.deepcopy(context.chat_data['map'])
    pos = context.chat_data['pos']
    frame[pos[1]][pos[0]] = 'I'
    theme = THEMES['default']
    frame = [[theme.get(x, 'X') for x in r] for r in frame]
    text = '\n'.join([''.join(l) for l in frame])
    kbd = Ikm([
        [Ikb(' ', callback_data=' '), Ikb('⬆️', callback_data='u'), Ikb(' ', callback_data=' ')],
        [Ikb('⬅️', callback_data='l'), Ikb('⬇️', callback_data='d'), Ikb('➡️', callback_data='r')]
    ])
    new_msg = {
        'quote': False,
        'parse_mode': "HTML",
        'text': f'<code>{text}</code>',
        'reply_markup': kbd
    }
    if context.chat_data.get('state') == 'won':
        new_msg['text'] = "Du hast gewonnen!"
        new_msg['reply_markup'] = None
    try:
        update.effective_message.edit_text(**new_msg)
    except Exception as e:
        print(e)
        update.effective_message.reply_text(**new_msg)


def callback(update, context):
    if update.callback_query.data in ['d', 'u', 'r', 'l']:
        move(update, context)


def move(update, context):
    print('moving')
    d = update.callback_query.data
    pos = context.chat_data['pos']
    if d == 'u':
        new_pos = [pos[0], pos[1] - 1]
    elif d == 'd':
        new_pos = [pos[0], pos[1] + 1]
    elif d == 'l':
        new_pos = [pos[0]-1, pos[1]]
    elif d == 'r':
        new_pos = [pos[0]+1, pos[1]]
    try:
        target = context.chat_data['map'][new_pos[1]][new_pos[0]]
        if target not in ['w']:
            context.chat_data['pos'] = new_pos
            logger.debug('position changed')
            if target == '1':
                context.chat_data['state'] = 'won'
            render(update, context)
        else:
            logger.debug('collided')
    except:
        logger.debug('target out of map')


def new_game(update, context):
    logger.debug('new game called')
    load_map(update, context)
    render(update, context)
cmds.append(new_game)
