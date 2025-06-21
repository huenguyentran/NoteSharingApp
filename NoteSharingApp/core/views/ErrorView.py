from django.shortcuts import render

def ErrorView(request, message="Đã xảy ra lỗi!", status=400):
    return render(request, 'error/error.html', {
        'message': message,
        'status_code': status
    }, status=status)
