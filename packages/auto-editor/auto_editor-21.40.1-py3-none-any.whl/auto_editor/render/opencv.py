'''render/opencv.py'''

import cv2
import numpy as np

import os.path

# Included Libraries
from auto_editor.interpolate import interpolate
from auto_editor.utils.progressbar import ProgressBar
from .utils import properties, scale_to_sped

def values(val, log, _type, total_frames, width, height):
    if(val == 'centerX'):
        return int(width / 2)
    if(val == 'centerY'):
        return int(height / 2)
    if(val == 'start'):
        return 0
    if(val == 'end'):
        return total_frames - 1
    if(val == 'width'):
        return width
    if(val == 'height'):
        return height

    if(not isinstance(val, int)
        and not (val.replace('.', '', 1)).replace('-', '', 1).isdigit()):
        log.error('Variable {} not implemented.'.format(val))
    return _type(val)

def _find_state(chunks, cframe):
    low = 0
    high = len(chunks) - 1

    while low <= high:
        mid = low + (high - low) // 2

        if(cframe >= chunks[mid][0] and cframe < chunks[mid][1]):
            return chunks[mid][2]
        elif(cframe > chunks[mid][0]):
            low = mid + 1
        else:
            high = mid - 1

    # cframe not in chunks
    return 0


def make_effects_sheet(effects, total_frames, width, height, log):
    effect_sheet = []
    for effect in effects:
        if(effect[0] == 'rectangle'):

            rectx1_sheet = np.zeros((total_frames + 1), dtype=int)
            recty1_sheet = np.zeros((total_frames + 1), dtype=int)
            rectx2_sheet = np.zeros((total_frames + 1), dtype=int)
            recty2_sheet = np.zeros((total_frames + 1), dtype=int)
            rectco_sheet = np.zeros((total_frames + 1, 3), dtype=int)
            rect_t_sheet = np.zeros((total_frames + 1), dtype=int)

            r = effect[1:]

            for i in range(6):
                r[i] = values(r[i], log, int, total_frames, width, height)

            rectx1_sheet[r[0]:r[1]] = r[2]
            recty1_sheet[r[0]:r[1]] = r[3]
            rectx2_sheet[r[0]:r[1]] = r[4]
            recty2_sheet[r[0]:r[1]] = r[5]
            rectco_sheet[r[0]:r[1]] = r[6]
            rect_t_sheet[r[0]:r[1]] = r[7]

            effect_sheet.append(
                ['rectangle', rectx1_sheet, recty1_sheet, rectx2_sheet, recty2_sheet,
                rectco_sheet, rect_t_sheet]
            )

        if(effect[0] == 'zoom'):

            zoom_sheet = np.ones((total_frames + 1), dtype=float)
            zoomx_sheet = np.full((total_frames + 1), int(width / 2), dtype=float)
            zoomy_sheet = np.full((total_frames + 1), int(height / 2), dtype=float)

            z = effect[1:]
            z[0] = values(z[0], log, int, total_frames, width, height)
            z[1] = values(z[1], log, int, total_frames, width, height)

            if(z[7] is not None): # hold value
                z[7] = values(z[7], log, int, total_frames, width, height)

            if(z[7] is None or z[7] > z[1]):
                zoom_sheet[z[0]:z[1]] = interpolate(z[2], z[3], z[1] - z[0], log,
                    method=z[6])
            else:
                zoom_sheet[z[0]:z[0]+z[7]] = interpolate(z[2], z[3], z[7], log,
                    method=z[6])
                zoom_sheet[z[0]+z[7]:z[1]] = z[3]

            zoomx_sheet[z[0]:z[1]] = values(z[4], log, float, total_frames, width, height)
            zoomy_sheet[z[0]:z[1]] = values(z[5], log, float, total_frames, width, height)

            effect_sheet.append(
                ['zoom', zoom_sheet, zoomx_sheet, zoomy_sheet]
            )
    return effect_sheet

def render_opencv(ffmpeg, inp, args, chunks, speeds, fps, has_vfr, effects, temp, log):
    if(has_vfr):
        cmd = ['-i', inp.path, '-map', '0:v:0', '-vf', 'fps=fps={}'.format(fps), '-r',
            str(fps), '-vsync', '1', '-f','matroska', '-vcodec', 'rawvideo', 'pipe:1']
        fileno = ffmpeg.Popen(cmd).stdout.fileno()
        cap = cv2.VideoCapture('pipe:{}'.format(fileno))
    else:
        cap = cv2.VideoCapture(inp.path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    spedup = os.path.join(temp, 'spedup.mp4')
    scale = os.path.join(temp, 'scale.mp4')

    if(args.scale != 1):
        width = int(width * args.scale)
        height = int(height * args.scale)
        video_name = scale
    else:
        video_name = spedup

    if(width < 2 or height < 2):
        log.error('Resolution too small.')
    log.debug('Resolution: {}x{}'.format(width, height))

    out = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    total_frames = chunks[len(chunks) - 1][1]
    cframe = 0

    cap.set(cv2.CAP_PROP_POS_FRAMES, cframe)
    remander = 0
    framesWritten = 0

    videoProgress = ProgressBar(total_frames, 'Creating new video',
        args.machine_readable_progress, args.no_progress)

    sheet = make_effects_sheet(effects, total_frames, width, height, log)

    while cap.isOpened():
        ret, frame = cap.read()
        if(not ret or cframe > total_frames):
            break

        for effect in sheet:
            if(effect[0] == 'rectangle'):

                x1 = int(effect[1][cframe])
                y1 = int(effect[2][cframe])
                x2 = int(effect[3][cframe])
                y2 = int(effect[4][cframe])

                if(x1 == y1 and y1 == x2 and x2 == y2 and y2 == 0):
                    pass
                else:
                    np_color = effect[5][cframe]
                    color = (int(np_color[0]), int(np_color[1]), int(np_color[2]))

                    t = int(effect[6][cframe])

                    frame = cv2.rectangle(frame, (x1,y1), (x2,y2), color, thickness=t)

            if(effect[0] == 'zoom'):

                zoom = effect[1][cframe]
                zoom_x = effect[2][cframe]
                zoom_y = effect[3][cframe]

                # Resize Frame
                new_size = (int(width * zoom), int(height * zoom))

                if(zoom == 1 and args.scale == 1):
                    blown = frame
                elif(new_size[0] < 1 or new_size[1] < 1):
                    blown = cv2.resize(frame, (1, 1), interpolation=cv2.INTER_AREA)
                else:
                    inter = cv2.INTER_CUBIC if zoom > 1 else cv2.INTER_AREA
                    blown = cv2.resize(frame, new_size, interpolation=inter)

                x1 = int((zoom_x * zoom)) - int((width / 2))
                x2 = int((zoom_x * zoom)) + int((width / 2))

                y1 = int((zoom_y * zoom)) - int((height / 2))
                y2 = int((zoom_y * zoom)) + int((height / 2))

                top, bottom, left, right = 0, 0, 0, 0

                if(y1 < 0):
                    top = -y1
                    y1 = 0
                if(x1 < 0):
                    left = -x1
                    x1 = 0

                frame = blown[y1:y2+1, x1:x2+1]

                bottom = (height + 1) - (frame.shape[0]) - top
                right = (width + 1) - frame.shape[1] - left
                frame = cv2.copyMakeBorder(
                    frame,
                    top = top,
                    bottom = bottom,
                    left = left,
                    right = right,
                    borderType = cv2.BORDER_CONSTANT,
                    value = args.background
                )

                if(frame.shape != (height+1, width+1, 3)):
                    # Throw error so that opencv dropped frames don't go unnoticed.
                    print('cframe {}'.format(cframe))
                    log.error('Wrong frame shape. Is {}, should be {}'.format(
                        frame.shape, (height+1, width+1, 3)))

        if(effects == [] and args.scale != 1):
            inter = cv2.INTER_CUBIC if args.scale > 1 else cv2.INTER_AREA
            frame = cv2.resize(frame, (width, height), interpolation=inter)

        cframe = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) # current frame

        state = _find_state(chunks, cframe)
        mySpeed = speeds[state]

        if(mySpeed != 99999):
            doIt = (1 / mySpeed) + remander
            for __ in range(int(doIt)):
                out.write(frame)
                framesWritten += 1
            remander = doIt % 1

        videoProgress.tick(cframe)
    log.debug('Frames Written: {}'.format(framesWritten))
    log.debug('Total Frames: {}'.format(total_frames))

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    if(args.scale == 1):
        cmd = properties(['-i', inp.path], args, inp)
        cmd.append(spedup)
        ffmpeg.run(cmd)
    else:
        scale_to_sped(ffmpeg, spedup, scale, inp, args, temp)

    return spedup
