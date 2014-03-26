(function($) {
    $(document).ready(function(){
        var loading = $('#loading');
        var users = [];
        $.getJSON("/api/v2/users", function(result) {
            var dropdown = $("#user_id");
            $.each(result, function(item) {
                dropdown.append($("<option />").val(item).text(this.name).attr('data-avatar', 'avatarurl'));
            });
            users = result;
            dropdown.show();
            loading.hide();
        });
        $('#user_id').change(function(){
            var selected_user = $("#user_id").val();
            var avatar = $('#user_id').data('avatar')
            var chart_div = $('#chart_div');
            if(selected_user) {
                var newImage = users[selected_user]['avatar'];
                $('#avatar').children('img').attr('src', newImage);
                loading.show();
                chart_div.hide();
                $.getJSON("/api/v1/presence_weekday/"+selected_user, function(result) {
                    var data = google.visualization.arrayToDataTable(result);
                    var options = {};
                    chart_div.show();
                    loading.hide();
                    var chart = new google.visualization.PieChart(chart_div[0]);
                    chart.draw(data, options);
                });
            }
        });
    });
})(jQuery);


// <option value='1' data-avatar='http://'>Name</option>
// .attr('data-avatar', this.info.avatar));