
function details()
{
	var r_commit = document.getElementById("id_radio_0");
	var r_patch  = document.getElementById("id_radio_1");
	var selected = document.getElementById("details");

	if(r_commit.checked == true)
	{
		selected.hidden = true;
	}

	if(r_patch.checked == true)
	{
		selected.hidden = false;
	}
}
