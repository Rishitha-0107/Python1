#program to find highest frequency charcter in a string
def highest_frequency_char(s):
    s=s.lower()
    mc=0
    mch= ''
    for i in range(len(s)):
        cnt=0
        for j in range(len(s)):
            if s[i]==s[j]:
                cnt+=1
        if cnt>mc:
            mc=cnt
            mch= s[i]
    print(f"Character with highest frequency: '{mch}' occurs {mc} times")
highest_frequency_char(input("Enter a string: "))