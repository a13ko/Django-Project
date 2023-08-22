from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from services.generator import CodeGenerator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.forms.widgets import ClearableFileInput

User = get_user_model()

# -----------------------   Admin Forms  ---------------------------------------------------


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(required=False,label="Şifrə", widget=forms.PasswordInput)
    password2 = forms.CharField(required=False,
        label="Şifrəni Doğrula", widget=forms.PasswordInput
    )
    email = forms.EmailField(required=False,label='Email')
    full_name =forms.CharField(required=False,label='Ad Soyad')
    username =forms.CharField(required=False,label='İstifadəçi Adı')

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "username",
            "password1",
            "password2",
        ]

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        email = self.cleaned_data.get("email")
        full_name = self.cleaned_data.get("full_name")
        username = self.cleaned_data.get("username")
        if password1 and password2 and password1 != password2:
            self.add_error('password1',"Sifreler eyni deyil")
        elif User.objects.filter(email=email).exists():
            self.add_error('email',"Bu email artıq qeydiyyatdan keçib.")
        elif User.objects.filter(username=username).exists():
            self.add_error('username',"Bu istifadəçi adı artıq mövcuddur.")
        elif full_name=="":
            self.add_error('full_name',"Ad boş qoyula bilməz")
        elif any(char.isdigit() for char in full_name):
            self.add_error('full_name',"Ad rəqəmdən ibarət olmamalıdır")
        elif email=="":
            self.add_error('email',"Email boş qoyula bilməz")
        elif username=="":
            self.add_error('username',"İstifadəçi adı boş qoyula bilməz")
        elif password1=="":
            self.add_error('password1',"Şifrə boş qoyula bilməz")       
        elif password2=="":
            self.add_error('password2',"Şifrə boş qoyula bilməz")
        elif len(password1.strip()) < 6:
            self.add_error('password1',"Şifrənin uzunluğu 6 dan böyük olmalıdır")   

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "is_active",
            "is_superuser",
            "password",
        ]

    def clean_password(self):
        return self.initial["password"]




# Login Form

class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Şifrə", widget=forms.PasswordInput,required=False)
    email = forms.EmailField(required=False,label='Email')

    class Meta:
        model = User
        fields = ("email", "password")


    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if User.objects.filter(email=email):
            user=User.objects.get(email=email)
            check_passwordr=check_password(password,user.password)
            if password=="":
                self.add_error('password',"Şifrə boş qoyula bilməz!")
            elif check_passwordr:
                if not user.is_active:
                    self.add_error('email', "Bu istifadəçi aktiv deyil...")
            else:
                self.add_error('email',"Email və ya Şifrə yanlışdır")

        elif email=="":
            self.add_error('email',"Email boş qoyula bilməz!")

        
            
        else:
            self.add_error('email',"Email və ya Şifrə yanlışdır")
        return self.cleaned_data


       

        
       


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': f'{self.fields[field].label}',
                'style':
                 ' text-align:left; padding:15px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; height: 50px; font-size: 16px; width: 100%;',
            })


class RegisterForm(UserAdminCreationForm):

    def save(self, commit=True):
        user = super(RegisterForm, self).save()
        user.set_password(self.cleaned_data.get("password1"))
        user.is_active = False
        user.activation_code = CodeGenerator.create_activation_link_code(
            size=4, model_=User
        )
        if commit:
            user.save()

        message = f"Please write code below: \n{user.activation_code}"

        # send mail
        send_mail(
            'Activate email', # subject
            message, # message
            settings.EMAIL_HOST_USER, # from email
            [user.email], # to mail list
            fail_silently=False,
        )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': f'{self.fields[field].label}',
                'style':
                 ' text-align:left; padding:15px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; height: 50px; font-size: 16px; width: 100%;',
            })



class ActivateForm(forms.ModelForm):
    activation_code = forms.CharField(required=False,label='Code')
    class Meta:
        model = User
        fields = ("activation_code", )

    def save(self, user):
        activation_code = self.cleaned_data.get("activation_code")
        if activation_code == user.activation_code:
            user.is_active = True
            user.activation_code = None
            user.save()
        
            
        return user

    def clean(self):
        activation_code = self.cleaned_data.get("activation_code")
        if activation_code=="":
            self.add_error('activation_code'," Boş qoyula bilməz!")
        elif not User.objects.filter(activation_code=activation_code).exists():
            self.add_error('activation_code'," Email və ya şifrə yanlışdır...")

        
        
        

       
        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': f'{self.fields[field].label}',
                'style':
                 ' text-align:left; padding:15px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; height: 50px; font-size: 16px; width: 100%;',
            })



class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': f'{self.fields[field].label}',
                'style':
                 ' text-align:left; padding:15px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; height: 50px; font-size: 16px; width: 100%;',
            })



class ResetPasswordForm(forms.ModelForm):
    email = forms.EmailField(required=False,label='Email')
    class Meta:
        model = User
        fields = ("email", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': f'{self.fields[field].label}',
                'style':
                 ' text-align:left; padding:15px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; height: 50px; font-size: 16px; width: 100%;',
            })

    def clean(self):
        email = self.cleaned_data.get("email")
        if email=="":
            self.add_error('email',"Email boş qoyula bilməz!")

        elif not User.objects.filter(email=email).exists():
            self.add_error('email',"Belə istifadəçi movcud deyil")
        

        

        return self.cleaned_data



class ResetPasswordCompleteForm(forms.ModelForm):
    password1 = forms.CharField(required=False,label="Şifrə", widget=forms.PasswordInput)
    password2 = forms.CharField(required=False,label="Şifrəni Doğrula", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': f'{self.fields[field].label}',
                'style':
                 ' text-align:left; padding:15px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; height: 50px; font-size: 16px; width: 100%;',
            })


    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1=="":
            self.add_error('password1',"Şifrə boş qoyula bilməz!")

        elif password2=="":
            self.add_error('password2',"Şifrə boş qoyula bilməz!")

        elif len(password1.strip()) < 6:
            self.add_error('password1',"Şifrənin uzunluğu minimum 6 simvol olmalıdır!")

        elif password1 != password2:
            self.add_error('password1',"Şifrələr eyni deyil...")

        

        return self.cleaned_data


    def save(self):
        password1 = self.cleaned_data.get("password1")
        self.instance.set_password(password1)
        self.instance.save()
        return self.instance


class UserDataChangeForm(forms.ModelForm):
    email = forms.EmailField(required=False, label='Email')
    full_name = forms.CharField(required=False, label='Tam Ad')
    username = forms.CharField(required=False, label='Istifadeci Adi')
    logo = forms.ImageField(required=False, label='Logo',widget=ClearableFileInput(attrs={'class':'hide-clear-button'}))

    class Meta:
        model = User
        fields = ('email', 'full_name', 'username', 'logo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            
            self.fields[field].widget.attrs.update({
                'placeholder': f'{self.fields[field].label}',
                'style':
                 ' text-align:left; padding:15px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; height: 50px; font-size: 16px; width: 100%;',
            })
            