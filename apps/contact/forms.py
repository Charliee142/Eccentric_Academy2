from django import forms


SUBJECT_CHOICES = [
    ('', '-- Select Subject --'),
    ('enrollment', 'Enrollment Inquiry'),
    ('technical', 'Technical Support'),
    ('billing', 'Billing & Payments'),
    ('partnership', 'Partnership'),
    ('other', 'Other'),
]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)
    message = forms.CharField(widget=forms.Textarea, max_length=2000, required=True)
    # Honeypot field (should be empty)
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 20:
            raise forms.ValidationError("Please provide more detail in your message.")
        return message

    def clean_website(self):
        """Honeypot – must be empty."""
        value = self.cleaned_data.get('website', '')
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '')
        if not subject:
            raise forms.ValidationError("Please select a subject.")
        return subject
