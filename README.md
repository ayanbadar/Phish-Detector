# Phish Detector 🔒

A Django-based web application that detects phishing URLs using deep learning. The application provides user authentication with WhatsApp OTP verification and a dashboard for URL analysis.

## 🚀 Features

- **Phishing URL Detection**: DL-powered URL analysis to identify potential phishing attempts
- **User Authentication**: Secure signup and login system
- **WhatsApp OTP Verification**: Two-factor authentication via WhatsApp messages
- **Modern Web Interface**: Clean, responsive dashboard for URL analysis
- **Real-time Analysis**: Instant results for URL safety assessment

## 🏗️ Architecture

- **Backend**: Django 5.1.4
- **Database**: MongoDB (users) + SQLite (Django)
- **DL Model**: TensorFlow/Keras neural network
- **Authentication**: Session-based with WhatsApp OTP
- **Frontend**: HTML templates with CSS styling

## 📁 Project Structure

```
phish_detector/
├── core/                          # Main Django app
│   ├── models.py                  # Database models
│   ├── views.py                   # Business logic and views
│   ├── forms.py                   # User input forms
│   ├── urls.py                    # URL routing
│   ├── phishing_model.h5         # Trained DL model
│   ├── tokenizer.pickle          # Text tokenizer for DL
│   ├── static/core/styles.css    # CSS styling
│   └── templates/                 # HTML templates
│       ├── signup.html           # User registration
│       ├── verify_otp.html       # OTP verification
│       ├── login.html            # User login
│       └── dashboard.html        # Main dashboard
├── phish_detector/               # Django project settings
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # Main URL routing
│   └── wsgi.py                   # WSGI configuration
└── manage.py                     # Django management script
```

## 🛠️ Prerequisites

- Python 3.8+
- MongoDB (running on localhost:27017)
- WhatsApp Web access (for OTP functionality)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd phish_detector
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   pip install pymongo
   pip install pywhatkit
   pip install tensorflow
   pip install numpy
   ```

4. **Set up MongoDB**
   - Ensure MongoDB is running on localhost:27017
   - The application will automatically create the required database and collections

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`

## 🔐 Usage

### User Registration
1. Navigate to the signup page
2. Fill in your details (name, email, phone, password)
3. Verify your phone number with WhatsApp OTP
4. Complete registration

### User Login
1. Use your registered email and password
2. Access the dashboard

### URL Analysis
1. In the dashboard, enter a URL to analyze
2. Click "Analyze" to get instant results
3. View the prediction: "Safe URL ✅" or "Phishing URL ❌"

## 🔧 Configuration

### WhatsApp Integration
- The application uses PyWhatKit for WhatsApp messaging
- Ensure you have WhatsApp Web access
- Phone numbers should be in the format: country code + number (e.g., +92XXXXXXXXXX)

### MongoDB Connection
- Default connection: `mongodb://localhost:27017/`
- Database: `security_app`
- Collection: `users`

### DL Model
- Pre-trained model: `core/phishing_model.h5`
- Tokenizer: `core/tokenizer.pickle`
- The model analyzes URL text patterns to detect phishing attempts

## 🚨 Security Features

- **OTP Verification**: WhatsApp-based two-factor authentication
- **Session Management**: Secure user sessions
- **Input Validation**: Form validation and sanitization
- **CSRF Protection**: Built-in Django CSRF protection

## 🧪 Testing

Run the Django test suite:
```bash
python manage.py test
```

## 🚀 Deployment

For production deployment:

1. **Update settings.py**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for sensitive data

2. **Static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database**
   - Use production-grade MongoDB
   - Configure proper authentication and network security

4. **Web server**
   - Use Gunicorn or uWSGI with Nginx
   - Configure SSL/TLS certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the Django debug logs
2. Verify MongoDB connection
3. Ensure WhatsApp Web is accessible
4. Check Python dependencies are correctly installed

## 🔮 Future Enhancements

- [ ] API endpoints for external integration
- [ ] Batch URL analysis
- [ ] Advanced DL model training
- [ ] User dashboard analytics
- [ ] Email notifications
- [ ] Mobile app support

## 📊 Model Performance

The phishing detection model uses:
- **Architecture**: Neural network with embedding layers
- **Input**: URL text sequences
- **Output**: Binary classification (safe/phishing)
- **Threshold**: 0.5 (configurable)

---

**Note**: This application is for educational and research purposes. Always verify security assessments through multiple sources in production environments.