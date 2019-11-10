<?php
require 'admin_startup.php';
require LIBDIR.'dbextra.php';

$usePk=auth('system');
$link = db_connect();
$file = __FILE__;

if (reqexists('add'))
{
    $comname = reqsval('comname');
    $datefrom = reqsval('datefrom');
    $dateto = reqsval('dateto');
    $location = reqsval('location');
    //$director = reqsval('director');
    $comptype = reqsval('comptype');
    $comcode = reqsval('code');
    $timeoffset = reqfval('timeoffset');
    $class = reqsval('comclass');

    if ($comname == '')
    {
        echo "<b>Can't create a competition with no name</b>";
    }
    else
    {
        # Insert new Comp in tblCompetition
        $query = "  INSERT INTO `tblCompetition` (
                        `comName`, `comLocation`, `comDateFrom`,
                        `comDateTo`, `comClass`,
                        `comType`, `comCode`, `comTimeOffset`
                    )
                    VALUES
                        (
                            '$comname', '$location', '$datefrom',
                            '$dateto', '$class', '$comptype',
                            '$comcode', $timeoffset
                        )";

        mysqli_query($link, $query) or die('Error ' . mysqli_errno($link) . ' Competition addition failed: ' . mysqli_connect_error());
        $comPk = mysqli_insert_id($link);

        $regarr = [];
        $regarr['comPk'] = $comPk;

        # Insert user as Admin for new comp
        $query = "  INSERT INTO `tblCompAuth`
                    VALUES
                        ($usePk, $comPk, 'admin')";
        //echo $query . "<br>";
        mysqli_query($link, $query) or die('Error ' . mysqli_errno($link) . ' CompAuth addition failed: ' . mysqli_connect_error());

        # Create ForComp entry
        $query = "  INSERT INTO `tblForComp` (`comPk`)
                    VALUES
                        ($comPk)";
        //echo $query . "<br>";
        mysqli_query($link, $query) or die('Error ' . mysqli_errno($link) . ' ForComp addition failed: ' . mysqli_connect_error());

        redirect("competition_admin.php?comPk=$comPk&created=1");
    }
}

if (reqexists('compscore'))
{
    $out = '';
    $retv = 0;
    $command = "python3 " . BINDIR . "create_comp_results.py $comPk";
    $pid = exec($command, $out, $retv);
    $ptime = microtime(true);
    # redirect to avoid Timeout if script takes too long
    sleep(35);
    // if ( script_isRunning($pid) )
    // {
    //     redirect("safe_process_admin.php?tasPk=$tasPk&comPk=$comPk&pid=$pid&time=$ptime&task=1");
    // }
    if (isset($out) and $out > 0) {
        $refPk = $out;
        $content .= "Event has been scored. <br /> \n
                        <a href='/comp_result.php?refPk=$refPk' target='_blank'>Check Generated Results</a> <br>\n
                        <a href='comp_result_admin.php?comPk=$comPk'>Comp Results Admin</a> <br>\n";
    }
    else {
        $content .= "There was an error scoring Event. <br /> \n";
    }
}

$comparr = [];
$comparr[] = array ('', fb('Date Range'), fb('Name'), fb('Class'), fb('Location'), fb('Director'), fb('External') );
$count = 1;

$sql = "SELECT * FROM `CompetitionView`";

$result = mysqli_query($link, $sql);
while($row = mysqli_fetch_assoc($result))
{
    $id = $row['comPk'];
    $name = $row['comName'];
    $datefrom = substr($row['comDateFrom'], 0, 10);
    $dateto = substr($row['comDateTo'], 0, 10);
    $today = time();
    $fromdate = strtotime($datefrom);
    $todate = strtotime($dateto) + 24*3600;
    $comclass = $row['comClass'];
    $ext = $row['comExt'] <> 0 ? "<strong>EXTERNAL EVENT</strong>" : null;
    $ext .= isset($row['comExtUrl']) ? ": <a href='".$row['comExtUrl']." target='_blank'>website</a>" : null;

    # Makes dates Bold if Comp is Now
    if ($today>=$fromdate && $today<=$todate)
    {
        $datestr = fb("$datefrom - $dateto");
    }
    else
    {
        $datestr = "$datefrom - $dateto";
    }

    $location = $row['comLocation'];
    $director = $row['comMeetDirName'];
    $comparr[] = array("$count.", $datestr, "<a href=\"competition_admin.php?comPk=$id\">" . $name . "</a>", $comclass, $location, $director, $ext);
    $count++;
}

# Create add comp form table
$compadd = [];

$compadd[] = array('Name', fin('comname', '', 20), 'Class:', fselect('comclass', 'PG', array('PG', 'HG', 'mixed')), 'Type:', fselect('comptype', 'RACE', array('RACE', 'Route', 'Team-RACE')));
$compadd[] = array('Abbreviation:', fin('code', '', 10), 'Date From:', fin('datefrom', '', 10), 'Date To:', fin('dateto', '', 10));
$compadd[] = array('Time Offset:', fin('timeoffset', '', 7), '', '', '', '');
$compadd[] = array(fis('add', 'Create Competition', '', '', '', '', '', ''));

//initializing template header
tpadmin($link,$file,$row);

echo "<form action=\"comp_admin.php\" name=\"compadmin\" method=\"post\">";
echo ftable($comparr, "", array('class="d"', 'class="l"'), '');
echo "<br><hr>";
echo "<h2>Scoring:</h2>";
echo "<form action=\"comp_admin.php?comPk=$comPk&tasPk=$tasPk\" name=\"compscore\" method=\"post\"> \n";
echo "<p class='explanation'>Score Comp will calculate from all tasks scored and published.<br>\n";
echo fis('compscore', 'Score Event', '');
echo "</form> \n";
echo "<br><hr>";
echo "<h2>Add Competition</h2>";
echo ftable($compadd, "", array('class="d"', 'class="l"'), '');
echo "</form>";

tpfooter($file);

?>
