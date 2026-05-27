// =========================
// CAPTCHA
// =========================

let currentCaptcha = "";

function generateCaptcha() {

    const chars =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    currentCaptcha = "";

    for (let i = 0; i < 6; i++) {

        currentCaptcha +=
            chars.charAt(
                Math.floor(Math.random() * chars.length)
            );
    }

    const captchaText =
        document.getElementById("captchaText");

    if (captchaText) {

        captchaText.innerText =
            currentCaptcha;
    }
}

generateCaptcha();


// =========================
// LOGIN
// =========================

const loginForm =
    document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener(
        "submit",

        async function (e) {

            e.preventDefault();

            const email =
                document.getElementById("email").value;

            const password =
                document.getElementById("password").value;

            const captchaInput =
                document.getElementById("captchaInput").value;

            if (captchaInput !== currentCaptcha) {

                alert("Invalid Captcha");

                return;
            }

            try {

                const response = await fetch(

                    "/login",

                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            email: email,

                            password: password
                        })
                    }
                );

                const data =
                    await response.json();

                if (response.ok) {

                    console.log(data);

                    console.log(data.token);

                    localStorage.setItem(
                    "token",
                      data.token
                    );

                    console.log(
                    localStorage.getItem("token")
                     );

                    alert("LOGIN SUCCESS");

                    window.location.href =
                    window.location.origin + "/dashboard";
                }

                else {

                    alert(data.error);
                }
            }

            catch (error) {

                console.log(error);
            }
        }
    );
}



// =========================
// REGISTER
// =========================

const registerForm =
    document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener(
        "submit",

        async function (e) {

            e.preventDefault();

            const data = {

                first_name:
                    document.getElementById("first_name").value,

                middle_name:
                    document.getElementById("middle_name").value,

                last_name:
                    document.getElementById("last_name").value,

                email:
                    document.getElementById("register_email").value,

                phone:
                    document.getElementById("phone").value,

                password:
                    document.getElementById("register_password").value
            };

            try {

                const response = await fetch(

                    "/customers",

                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify(data)
                    }
                );

                const result =
                    await response.json();

                if (response.ok) {

                    alert("Registration Successful");

                    window.location.href = "/";
                }

                else {

                    alert(result.error);
                }
            }

            catch (error) {

                console.log(error);
            }
        }
    );
}



// =========================
// DASHBOARD SECURITY
// =========================

const token =
    localStorage.getItem("token");

if (

    !token &&
    window.location.pathname ===
    "/dashboard"

) {

    window.location.href = "/";
}



// =========================
// SIDEBAR SECTION SWITCHING
// =========================

function showSection(sectionId) {

    const sections =
        document.querySelectorAll(".section");

    sections.forEach(section => {

        section.classList.add("hidden");
    });

    document
        .getElementById(sectionId)
        .classList.remove("hidden");
}



// =========================
// LOAD ACCOUNTS
// =========================

async function loadAccounts() {

    try {

        const response = await fetch(

            "/accounts",

            {

                method: "GET",

                headers: {

                    "Authorization":
                        "Bearer " + token
                }
            }
        );

        const data =
            await response.json();

        const accountsContainer =
            document.getElementById(
                "accounts-container"
            );

        if (!accountsContainer) return;

        accountsContainer.innerHTML = "";

        let totalBalance = 0;

        data.forEach(account => {

            totalBalance +=
                parseFloat(account.balance);

            accountsContainer.innerHTML += `

                <div class="account-card">

                    <h2>
                        ${account.account_type}
                    </h2>

                    <p>
                        Account ID:
                        ${account.account_id}
                    </p>

                    <p>
                        Balance:
                        ₹${account.balance}
                    </p>

                    <p>
                        Branch:
                        ${account.branch_id}
                    </p>

                </div>
            `;
        });

        document.getElementById(
            "total-balance"
        ).innerText =
            "₹" + totalBalance;

        document.getElementById(
            "total-accounts"
        ).innerText =
            data.length;
    }

    catch (error) {

        console.log(error);
    }
}



// =========================
// LOAD TRANSACTIONS
// =========================

async function loadTransactions() {

    try {

        const response = await fetch(

            "/transactions",

            {

                method: "GET",

                headers: {

                    "Authorization":
                        "Bearer " + token
                }
            }
        );

        const data =
            await response.json();

        const table =
            document.getElementById(
                "transactions-table-body"
            );

        if (!table) return;

        table.innerHTML = "";

        data.forEach(transaction => {

            table.innerHTML += `

                <tr>

                    <td>
                        ${transaction.transaction_id}
                    </td>

                    <td>
                        ${transaction.transaction_type}
                    </td>

                    <td>
                        ₹${transaction.amount}
                    </td>

                </tr>
            `;
        });
    }

    catch (error) {

        console.log(error);
    }
}



// =========================
// DEPOSIT
// =========================

async function depositMoney() {

    const accountId =
        document.getElementById(
            "deposit-account-id"
        ).value;

    const amount =
        document.getElementById(
            "deposit-amount"
        ).value;

    try {

        const response = await fetch(

            "/deposit",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json",

                    "Authorization":
                        "Bearer " + token
                },

                body: JSON.stringify({

                    account_id: accountId,

                    amount: amount
                })
            }
        );

        const data =
            await response.json();

        if (response.ok) {

            alert(
                data.message || "Deposit successful"
            );

            await loadAccounts();

            await loadTransactions();

        }

        else {

            alert(
                data.error || "Deposit failed"
            );
        }

    }

    catch (error) {

        console.log(error);

        alert("Server error");
    }
}



// =========================
// WITHDRAW
// =========================

async function withdrawMoney() {

    const accountId =
        document.getElementById(
            "withdraw-account-id"
        ).value;

    const amount =
        document.getElementById(
            "withdraw-amount"
        ).value;

    try {

        const response = await fetch(

            "/withdraw",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json",

                    "Authorization":
                        "Bearer " + token
                },

                body: JSON.stringify({

                    account_id: accountId,

                    amount: amount
                })
            }
        );

        const data =
            await response.json();

        if (response.ok) {

            alert(
                data.message || "Withdraw successful"
            );

            await loadAccounts();

            await loadTransactions();

        }

        else {

            alert(
                data.error || "Withdraw failed"
            );
        }

    }

    catch (error) {

        console.log(error);

        alert("Server error");
    }
}


// =========================
// TRANSFER
// =========================

async function transferMoney() {

    const sender =
        document.getElementById(
            "sender-account-id"
        ).value;

    const receiver =
        document.getElementById(
            "receiver-account-id"
        ).value;

    const amount =
        document.getElementById(
            "transfer-amount"
        ).value;

    try {

        const response = await fetch(

            "/transfer",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json",

                    "Authorization":
                        "Bearer " + token
                },

                body: JSON.stringify({

                    sender_account_id:
                        sender,

                    receiver_account_id:
                        receiver,

                    amount: amount
                })
            }
        );

        const data =
            await response.json();

        if (response.ok) {

            alert(
                data.message || "Transfer successful"
            );

            await loadAccounts();

            await loadTransactions();

        }

        else {

            alert(
                data.error || "Transfer failed"
            );
        }

    }

    catch (error) {

        console.log(error);

        alert("Server error");
    }
}



// =========================
// LOGOUT
// =========================

function logoutUser() {

    localStorage.removeItem("token");

    window.location.href = "/";
}



// =========================
// INITIAL DASHBOARD LOAD
// =========================

if (

    window.location.pathname ===
    "/dashboard"

) {

    loadAccounts();

    loadTransactions();
}
// =========================
// CHATBOT TOGGLE
// =========================

function toggleChatbot() {

    const chatbot =
        document.getElementById(
            "chatbot-container"
        );

    chatbot.classList.toggle("hidden");
}



// =========================
// AI CHATBOT
// =========================

async function sendMessage() {

    const input =
        document.getElementById(
            "chat-input"
        );

    const message =
        input.value.trim();

    if (!message) return;

    const chatMessages =
        document.getElementById(
            "chat-messages"
        );

    // USER MESSAGE

    chatMessages.innerHTML += `

        <div class="user-message">

            ${message}

        </div>
    `;

    input.value = "";

    try {

        const response = await fetch(

            "https://ai-chatbot-flask-3ut3.onrender.com/api/chat",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    message: message
                })
            }
        );

        const data =
            await response.json();

        chatMessages.innerHTML += `

            <div class="bot-message">

                ${data.response}

            </div>
        `;

        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }

    catch (error) {

        console.log(error);

        chatMessages.innerHTML += `

            <div class="bot-message">

                AI server error

            </div>
        `;
    }
}
function openAIChatbot() {

    window.open(
        "https://ai-chatbot-flask-3ut3.onrender.com/",
        "_blank"
    );
}

function showAssistantResponse(type) {

    let response = "";



    if(type === "deposit") {

        response = `
            <h3>💰 Deposit Money</h3>

            <p>
                To deposit money:
            </p>

            <ul>
                <li>Go to Deposit section</li>
                <li>Enter amount</li>
                <li>Click Deposit button</li>
            </ul>
        `;
    }



    else if(type === "withdraw") {

        response = `
            <h3>💸 Withdraw Money</h3>

            <p>
                To withdraw money:
            </p>

            <ul>
                <li>Go to Withdraw section</li>
                <li>Enter amount</li>
                <li>Click Withdraw button</li>
            </ul>
        `;
    }



    else if(type === "transfer") {

        response = `
            <h3>🔄 Transfer Money</h3>

            <p>
                To transfer money:
            </p>

            <ul>
                <li>Go to Transfer section</li>
                <li>Enter receiver account ID</li>
                <li>Enter amount</li>
                <li>Click Transfer button</li>
            </ul>
        `;
    }



    else if(type === "balance") {

        response = `
            <h3>📊 View Balance</h3>

            <p>
                Your total balance is displayed
                on the dashboard home page.
            </p>
        `;
    }



    else if(type === "transactions") {

        response = `
            <h3>📜 View Transactions</h3>

            <p>
                Open Transactions section
                from sidebar menu to view
                complete transaction history.
            </p>
        `;
    }



    else if(type === "accounts") {

        response = `
            <h3>🏦 Account Information</h3>

            <p>
                Your linked bank accounts
                are displayed inside
                the Accounts section.
            </p>
        `;
    }



    document.getElementById(
        "assistant-response"
    ).innerHTML = response;
}
async function changePassword() {

    const oldPassword =
        document.getElementById(
            "oldPassword"
        ).value;

    const newPassword =
        document.getElementById(
            "newPassword"
        ).value;

    const token =
        localStorage.getItem("token");

    const response = await fetch(
        "/change-password",
        {
            method: "PUT",

            headers: {

                "Content-Type":
                    "application/json",

                "Authorization":
                    `Bearer ${token}`
            },

            body: JSON.stringify({

                old_password: oldPassword,

                new_password: newPassword
            })
        }
    );

    const data = await response.json();

    alert(data.message || data.error);
}