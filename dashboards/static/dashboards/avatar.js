"use strict";

// Selecting elements using jQuery
const $avatar = $("#avatars");
const $avatarList = $avatar.find("#list");
const $avatarSubmit = $avatar.find("#submit");
const $avatarForm = $avatar.find("#form");

/**
 * Fetch avatars from the server and display them in the UI.
 */
function fetchAvatars() {
    $.ajax({
        url: avatar_url,
        type: "GET",
        dataType: "json",
        success: function (avatars) {
            avatars.forEach(function (avatar) {
                const $avatarItem = $(`
                    <div class="avatar-preview-item">
                        <input type="radio" name="avatar" id="avatar-${avatar.id}" value="${avatar.id}">
                        <label for="avatar-${avatar.id}">
                            <img src="${avatar.image}" alt="Avatar ${avatar.id}">
                        </label>
                    </div>
                `);

                $avatarList.append($avatarItem);
            });
        },
        error: function (xhr, status, error) {
            console.error("Error fetching avatars:", error);
        }
    });
}

/**
 * Update the user's avatar with the selected one.
 * @param {Object} data - The data containing user ID and selected avatar ID.
 */
function updateAvatar(data) {
    $.ajax({
        url: update_avatar_url,
        type: "PATCH",
        contentType: "application/json",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: JSON.stringify(data),
        success: function () {
            location.reload();
        },
        error: function (xhr, status, error) {
            console.error("Error updating avatar:", error);
        }
    });
}

/**
 * Handle the avatar update when the submit button is clicked.
 */
function handleAvatarUpdate() {
    const $selectedAvatar = $avatarForm.find("input[name='avatar']:checked");

    if ($selectedAvatar.length) {
        const selectedAvatarId = $selectedAvatar.val();
        const formData = {
            id: student_id,
            avatar: selectedAvatarId,
        };

        updateAvatar(formData);
    } else {
        console.log("No avatar selected.");
    }
}

// Event listener for the avatar submit button
$avatarSubmit.on("click", function (event) {
    event.preventDefault();
    handleAvatarUpdate();
});

// Function to be called when the document is ready
$(document).ready(function () {
    fetchAvatars();
});
