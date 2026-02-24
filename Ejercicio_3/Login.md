# Login

Login

Primero se inicializan las variables con la cuenta y contraseña y la variable intentos

Se abre un while para limitar los intentos a 3

Primero se pregunta a terminal, cual es el usuario, después se checa si en su composición no esta vacio o con algún espacio, de ser detectado se manda mensaje a terminal sobre el error y se suma un intento, de no ser así continua con la contraseña, se pregunta la contraseña y se checa si cuenta con mínimo una letra y un numero, si no se regresa al inicio y suma un intento, si no, también se checa si el largo de la contraseña, si no es mínimo de 8 caracteres se detecta, se mandas mensaje a terminal del error y se vuelve a empezar con  un intento menos, por ultimo se checa si el usuario y contraseña son correctos; si si lo son se concede acceso, si no se pide que lo intente de nuevo y se le suma otro intento, pasados 3 intentos fallidos, se cierra el programa.