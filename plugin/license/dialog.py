import gettext
_ = lambda m: gettext.dgettext(message=m, domain='ovirt-engine-setup')


from otopi import util

@util.export
def validate_license(dialog,name,note,hint,prompt=True):
    #print note
    def queryValue_Str(name, hint,*note):
        hint="("+hint+")" if hint else ''
        dialog.note(text=hint+note[0])
        value = dialog._readline()
        return value


    #    hint="("+hint+")" if hint else ''
    #    name = raw_input(hint+note[0]);
    #    license = raw_input(note[1]); 
 
    #    return name,license


    return queryValue_Str(name,hint,*note)

