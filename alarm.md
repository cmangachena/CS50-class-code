# False Alarm

## Questions

2.1. There is incosistent use of lowercase and uppercase letters.
     The use of the dash is inconsistent (DRILL-PACOM (DEMO) STATE ONLY) and the list would be better to use if it was in alphabetical order.

2.2. The UI is to blame because the way it is structured has no order and is not easy to use. The background is not highlighted and all the textstyle and colour looks the same such that it is very likely
     the human will click on the wrong one.

2.3a. I would use the, header feature for the "STATE EOC" part and "TEXT MESSAGE" part, using the tags (<h1></h1>),(<h2></h2>) respectively
      and "ordered list feature"(<ol><li></li></ol>) to put the links into a list.

2.3b. I would use css selectors to colour code and code the list e.g using the element selector, color coding each element of the list.
      I would use the li: nth-child(1) up to li:nth-child(n), the n inside the braces being the last link on the list. I would use the color: green style function for example to colour code each link.

2.3c. I would use the javascript pop uo alert feature to alert the user everytime they click a link. This alert would ask the user if they are certain they want to perfom that action.
      for example using information from w3 schools:
      <script>
        function when_link_is_clicked() {
        alert("You are about to send an alarm! Are you sure you would like to perform this action?");
         }
     </script> and embed it within the html i write for the page.


2.4. For the purpose of recording all the instances when the link was clicked and user clicked yes or no when the alert popped up.
     I would use the sql INSERT INTO feature to achieve this.

2.5. If the user clicks on link then clicks yes on alert message that pops up without reading the alert or going back to make sure the link they chose was the correct one.

## Debrief

a. w3 schools, google

b. 30 minutes
