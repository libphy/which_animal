import os
import subprocess

def convert2wav(directory): # convert non-.wav audio files to .wav files using ffmpeg
    # When converting, my standard options are: sampling rate 22050 Hz, 1 channel
    audioformats = ['mp3','flac','ogg','aiff','aif']
    fileslist = os.listdir(directory)
    subprocess.check_output(['bash','-c', 'mkdir '+directory+'/standard'])
    bashCommandlist = filter(None,map(lambda name: 'ffmpeg -i '+ directory + '/'+ name + ' -ar 22050 -ac 1 '+ directory+'/standard/'+ name.split('.')[0]+'.wav' if str(name.split('.')[1]) in audioformats else None, fileslist))
    for command in bashCommandlist:
        subprocess.check_output(['bash','-c', command])
    print '.wav conversion done'

def dsmono(directory,filename): #downsample to 22050 Hz and change stereo to mono
    if not os.path.isdir(directory+'/down_mono'):
        os.makedirs(directory+'/down_mono')
    command = 'ffmpeg -i '+directory+'/'+filename+' -ar 22050 -ac 1 '+directory+'/down_mono/'+filename
    subprocess.check_output(['bash','-c',command])

def movewavfiles(directory): #move all .wav files into a subfolder named wav.
    if not os.path.isdir(directory+'/wav'):
        os.makedirs(directory+'/wav')
    command = 'mv '+directory+'/*.wav '+directory+'/wav/'
    print command
    subprocess.check_output(['bash','-c', command])
    print 'wav files moved'

def movefiles(directory,filename,sub): #move any file to a specified subdirectory
    if not os.path.isdir(directory+'/'+sub):
        os.makedirs(directory+'/'+sub)
    command = 'mv '+directory+'/'+filename+' '+directory+'/'+sub+'/'+filename
    print command
    subprocess.check_output(['bash','-c', command])

def rename(directory,tag): #rename audio files and save the name change log as pickle
    fileslist = os.listdir(directory)
    newfileslist=map(lambda i: tag+ '_' + str(i) + '.' + fileslist[i].split('.')[1],range(len(fileslist)))
    log = zip(fileslist,newfileslist)
    with open( 'renamed_'+tag+'.pkl', "w" ) as f:
        pickle.dump(log, f)
    print directory
    for old, new in log:
        os.rename(directory+'/'+old,directory+'/'+new)
    print 'rename done'
