from flask import Blueprint,render_template,url_for,redirect


mod = Blueprint('minderfiles', __name__,
                        template_folder='static/minder')

#
# @mod.route('/ui/<path:args>', methods=['GET'])
# def get_minderfile(args):
#     print(args)
#     return render_template('minder/ui/'+ args)

#
@mod.route('/ui/<path:args>', methods=['GET'])
def get_minderfile(args):
    print(args)
    args = args.split('/')
    folder = '/static/minder/ui/'
    for i in range(len(args)):
        if i<len(args)-1:
            folder = folder+args[i]+'/'
        else:
            # filaname = args[i]
            folder = folder + args[i]
    print(folder)
    return redirect(folder)\

@mod.route('/src/<path:args>', methods=['GET'])
def get_minderfile1(args):
    print(args)
    args = args.split('/')
    folder = '/static/minder/src/'
    for i in range(len(args)):
        if i<len(args)-1:
            folder = folder+args[i]+'/'
        else:
            # filaname = args[i]
            folder = folder + args[i]
    print(folder)
    return redirect(folder)