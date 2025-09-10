#program to find lowestfrequency charcter in a string
def lfc(s):
    s=s.lower()
    mc=len(s)+1
    mch= ''
    for i in range(len(s)):
        cnt=0
        for j in range(len(s)):
            if s[i]==s[j]:
                cnt+=1
        if cnt<mc:
            mc=cnt
            mch=s[i]
    print(f"Character with lowest frequency: '{mch}' occurs {mc} times")
lfc(input("Enter a string: "))