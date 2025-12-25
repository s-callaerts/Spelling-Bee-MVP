//Simple redirecting from index to log in or register

const login = document.getElementById("login");

login.addEventListener("click", () => window.location.href="./login.html");

const register = document.getElementById("register");

register.addEventListener("click", () => window.location.href="./signup.html");
