def print_result(request,task):
    result = task.result
    return render(request, 'dialog.html', locals())