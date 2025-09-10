#program to count occurences of a character in a given string
def freq_string(s):
    result= ""
    for i in range(len(s)):
        if s[i] in s[:i]:   
            continue
        count=0
        for j in s:
            if j==s[i]:
                count+=1
        result+=s[i]+str(count)
    print(result)
s="rishitha"
freq_string(s)

