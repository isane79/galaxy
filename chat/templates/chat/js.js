const modalSidebar = document.getElementById("modal-sidebar");

const chatsSpan = document.getElementById("chats");
const closeModalButton = document.getElementById("close-modal");

chatsSpan.addEventListener("click", () => {
    modalSidebar.classList.toggle("hidden");
});
closeModalButton.addEventListener("click", () => {
    modalSidebar.classList.toggle("hidden");
});


function scrollToBottom() {
    const container = document.getElementById("chat-area");
    container.scrollTop = container.scrollHeight;
}
scrollToBottom();


let currentChatRoomName = null;

const socket = new WebSocket(
    `ws://${window.location.host}/ws/chat/`
);

socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    const chatMessages = document.getElementById("chat-messages");
    chatMessages.innerHTML += data.html;
    scrollToBottom();
});

const form = document.getElementById("chat_message_form");

form.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    const message = {
        type: "message",
        chatroom_name: currentChatRoomName,
        content: formData.get("content"),
    };
    socket.send(JSON.stringify(message));
    form.reset();
});

document.querySelectorAll(".chat-room").forEach((chatRoom) => {
    chatRoom.addEventListener("click", () => {
        modalSidebar.classList.add("hidden");

        currentChatRoomName = chatRoom.dataset.chatId;

        socket.send(
            JSON.stringify({
                type: "switch_chat",
                new_chatroom_name: currentChatRoomName,
            })
        );

        const chatMessages = document.getElementById("chat-messages");
        chatMessages.innerHTML = "";

        const chatName = document.getElementById("chat-name");
        chatName.innerHTML = `Chatting with <b>${chatRoom.dataset.chatName}</b>`;

    });
});


