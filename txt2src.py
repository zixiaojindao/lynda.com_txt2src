import os
import re

def GetValidPathChars(pathChars):
    return  re.sub("[<>:\?\"/\\\|\*]+", " ", pathChars).strip()

def Cleaning(orgLines):
    retLines = []
    for i in range(len(orgLines)):
        if(orgLines[i].strip() == "Introduction"):
            orgLines[i] = "0. Introduction"
            break
    for j in range(i, len(orgLines)):
        if(orgLines[j].strip() != ""):
            if(orgLines[j].strip() == "Conclusion"):
                orgLines[j] =  "9. Conclusion"
            retLines.append(orgLines[j].strip())
    return retLines

def TranslateSection(basePath, chapterIndex, sectionIndex, content, index):
    if(index >= len(content)):
        return index
    sentenceId = 1
    sectionFileName = "{:0>2d}{:0>2d}".format(chapterIndex, sectionIndex) +  " " + GetValidPathChars(content[index])
    index += 1
    with open(basePath + "\\" + sectionFileName + ".srt", "w") as f:
        while index < len(content):
            if content[index] == "Collapse this transcript":
                index += 1
                break
            #print(content[index])
            currentSentence = content[index]
            nextSentence = content[index + 1]
            if nextSentence[0][0].isdigit():
                endTime = ("00:" + nextSentence[0:5] + ",000")
            else:
                endTime = ("99:59:59,000")
            f.write(str(sentenceId) + "\n")
            timeIndex = ""
            timeIndex += ("00:" + currentSentence[0:5] + ",000")
            timeIndex += (" --> ")
            timeIndex += endTime
            f.write(timeIndex + "\n")
            f.write(currentSentence[5:].strip()+ "\n")
            f.write("\n")
            sentenceId += 1
            index += 1
    return index

def isEndofChapter(content, index):
    if index >= len(content) - 1:
        return False
    nextLine = content[index + 1]
    if(len(nextLine) < 5):
        return True
    if(nextLine[0].isdigit() and nextLine[1].isdigit() and nextLine[2] == ':' and nextLine[3].isdigit() and nextLine[4].isdigit()):
        return False
    return True

def TranslateChapter(basePath, chapterIndex, content, index):
    if(index >= len(content)):
        return index
    if content[index][0].isdigit():
        chapterTitle = content[index][content[index].find('.') + 1:].strip()
    else:
        chapterTitle = content[index]
    formatChapterIndex = "{:0>2d}".format(chapterIndex)
    chapterDirectoryName = formatChapterIndex + " " + GetValidPathChars(chapterTitle)
    currentChapterPath = basePath + "\\" + chapterDirectoryName
    if not os.path.exists(currentChapterPath):
        print(currentChapterPath)
        os.mkdir(currentChapterPath)
    index += 1
    sectionIndex = 1
    while index < len(content):
        index = TranslateSection(currentChapterPath, chapterIndex, sectionIndex, content, index)
        sectionIndex += 1
        if isEndofChapter(content, index):
            break
    return index


def TranslateCourse(fileName):
    with open(fileName, "r") as f:
        allLines = f.readlines()
    content = Cleaning(allLines)
    courseName = GetValidPathChars(fileName[0:fileName.find("字幕")])
    if(not os.path.exists(courseName)):
        os.mkdir(courseName)
    chapterIndex = 0
    index = 0
    while index < len(content):
        index = TranslateChapter(courseName, chapterIndex, content, index)
        chapterIndex += 1

if __name__ == "__main__":
    errorList = []
    try:
        for file in os.listdir("."):
            if os.path.splitext(file)[1] == ".txt":
                print(file)
                TranslateCourse(file)
    except BaseException as e:
        errorList.append(file)
    print("error list")
    for errorFile in errorList:
        print(errorFile)
