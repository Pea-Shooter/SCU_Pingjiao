from django import forms
from django.forms import widgets


class PostUserData(forms.Form):
    """Include some user input

    stu_id: the school id of each student
    stu_passwd: the password which attached with each school-id
    """

    stu_id = forms.CharField(required=True, label='Student ID', error_messages={
        'required': 'Student ID is required!',
        'id_check': 'Student ID must be 11 digits!'
    }, widget=widgets.TextInput(attrs={'placeholder': 'Enter your student id at here', 'class': 'form-control input-lg'}))

    passwd = forms.CharField(required=True, label='Password', error_messages={
        'required': 'Passwdord is required!'
    }, widget=widgets.PasswordInput(attrs={'placeholder': 'Enter your password at here', 'class': 'form-control input-lg'}))

    def clean(self):
        """Clean-function will handle some error, and raise error_message to templates

        Examples:
        1. if the stu_id is not 11 digits, raise error_message
        2. if the stu_id is blank, raise error
        3. if passwd is blank, raise error
        """

        cleaned_data = super(PostUserData, self).clean()
        stu_id = cleaned_data.get('stu_id')
        passwd = cleaned_data.get('passwd')

        if stu_id and self.check_format(stu_id) is False:
            temp = self.fields['stu_id']
            raise forms.ValidationError(self.fields['stu_id'].error_messages['id_check'], code='stu_id')

        return cleaned_data

    def check_format(self, stu_id):
        try:
            if len(stu_id) < 11:
                return False
            test = int(stu_id)
            return True
        except Exception:
            return False
