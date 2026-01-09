//Simple redirecting from index to log in or register

const login = document.getElementById("login");

login.addEventListener("click", () => window.location.href="/login_page");

const register = document.getElementById("register");

register.addEventListener("click", () => window.location.href="/signup_page");
