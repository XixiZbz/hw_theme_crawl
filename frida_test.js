
Java.perform(function () {
        var hook_1 = Java.use('com.vivo.security.e');
        hook_1.bh.implementation = function(a){
                console.log("fuck",a);
                console.log(this.str1);
                return a
        };

        var hook = Java.use('com.bbk.theme.payment.utils.VivoSignUtils');
        hook.vivoEncrypt.implementation = function(a){
                this.uz = false;
                console.log("fuck",a,this.encryptKey(a));
                return this.encryptKey(a)
        };

        // var hook = Java.use('com.bbk.theme.e.a');
        // hook.md5.overload("java.lang.String","java.lang.String").implementation = function(a){
        //         console.log("fuck",a);
        //         console.log(arguments[0]);
        //         return this.md

    }
)
