
def loadData(uri):
    with open(uri) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line

    content = [x.strip() for x in content]
    content=content[:len(content)//180]
    print("len content",len(content))
    return content
