$(document).ready(function(){
    var pusher = new Pusher('9f04d3ecab45dc1b9f18');
    var miniming = pusher.subscribe('presence-miniming');

    miniming.bind("pusher:subscription_succeeded", function(members){
        console.log("A new comer!")
        members.each(function(member){
            $("#current_users").append("<li id='member_" + member.id + "'>" + member.info.username + "</li>");
        })

    })

    miniming.bind("pusher:member_added", function(member){
        console.log("new member!")
        $(".messages").append(member.info.username + " 님이 입장함!");
        $(".users").append("<li id='member_" + member.id + "'>" + member.info.username + "</li>")
    })

    miniming.bind("pusher:member_removed", function(member){
        console.log("a member has gone!")
                            // $("#member.id").remove();
                            $("#member_"+member.id).remove();
                            console.log("what?")
                            $(".messages").append(member.info.username + " 님이 나가버림!");
                        })

    miniming.bind('new_message', function(data){
        $(".messages").append("<p>" + data.username + ":" + data.message + "&hearts;" + " 작성시간:" + data.time + "</p>")
        $(".messages").val("")
    });

    $("#submitMessage").click(function(){
        $.ajax({
            url: "/new_message",
            type: "POST",
            dataType: "JSON",
            data: {
                message: $("#inputMessage").val()
            },
            success: function(data){
                if(data.success){
                    console.log("Successfully sent new message!")
                }
                else{
                    console.log("Failed to send new message!")
                }
            },
            error: function(data){
                console.log("Server error! T~T")
            }
        });
    });
});
