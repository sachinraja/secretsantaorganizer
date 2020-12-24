let offset = 12

function loadMoreGroups(button)
{
    button.disabled = true;
    button.value = "Loading...";

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/get-group-titles")
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(
        {
            "offset" : offset
        }));

    xhr.onload = function(){
        if (xhr.status == 200){
            offset += 12;
            let groups = JSON.parse(xhr.responseText)
            if (groups.length === 0){
                error(button.parentElement, "All groups have already been loaded.");
                button.disabled = false;
                button.value = "Load More";
                return;
            }

            let groupContainer = document.getElementById("groups");

            for ([group_id, group_title] of groups){
                let newGroup = document.createElement("div");

                let groupTitleHeader = document.createElement("h2");
                groupTitleHeader.textContent = group_title;
                newGroup.appendChild(groupTitleHeader)

                let groupManageButton = document.createElement("a");
                groupManageButton.className = "redButton";
                groupManageButton.href = `/group/${group_id}`;
                groupManageButton.textContent = "Manage";
                newGroup.appendChild(groupManageButton);

                groupContainer.appendChild(newGroup);
            }
        }

        else{
            error(button, "Unable to load more groups.");
        }

        button.disabled = false;
        button.value = "Load More";
    }
}
