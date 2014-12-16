def aaa(name,hint,note):
    def queryValue_Str(name, hint,*note):
        hint="("+hint+")" if hint else ''
        name = raw_input(hint+note[0]);
        license = raw_input(note[1]); 
 
        return name,license
    queryValue_Str(name,hint,*note)

bb=('Please enter your license name:', 'Please Enter your license:')
aaa("d","dd",bb)


