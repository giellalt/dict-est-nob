#!/usr/bin/perl -w
use utf8 ;

# Simple script to convert csv to xml
# For input/outpus examples, see below.


print STDOUT "<r>\n";
http://www.google.no/imgres?imgurl=http%3A%2F%2F1.vgc.no%2Fdrpublish%2Fimages%2Farticle%2F2014%2F02%2F07%2F23047658%2F1%2F990%2F2067193.jpg&imgrefurl=http%3A%2F%2Fwww.vg.no%2Fsport%2Flangrenn%2Fol-2014%2Fastrid-uhrenholdt-jacobsen-mistet-broren%2Fa%2F10121931%2F&h=675&w=990&tbnid=KYDEczl1Ier0bM%3A&zoom=1&docid=Dj4NTTsM-27CEM&ei=4DLrU9PkCY_34QT914GoDg&tbm=isch&client=safari&ved=0CEoQMyglMCU&iact=rc&uact=3&dur=427&page=2&start=28&ndsp=25
while (<>) 
{
	chomp ;
#	my ($me+, se+, pe+, ge+, ls+, lg+´, tp+, rs+, rg+, sl+, ht+, ::+, nr+, de+, sl+, ht+, nn+, pl+, gn+, sn+, kn+, fe+, pe+, de0, sl+, ht+, fn+, pl+, gn+, sn+, kn+) = split /\t/ ;
	my ($lemma, $POS, $trans) = split /\t/ ;
	print STDOUT "   <e src=\"neen\">\n";
	print STDOUT "      <lg>\n";
	print STDOUT "         <l pos=\"N\">$lemma</l>\n";
	print STDOUT "      </lg>\n";
	print STDOUT "      <mg>\n";
	print STDOUT "         <tg>\n";
	print STDOUT "            <t pos=\"$POS\" gen=\"x\">$trans</t>\n";
#	print STDOUT "            <t pos=\"$POS\">$trans2</t>\n";
#	print STDOUT "            <t pos=\"$POS\">$trans3</t>\n";
	print STDOUT "         </tg>\n";
	print STDOUT "      </mg>\n";
	print STDOUT "   </e>\n";
}

print STDOUT "</r>\n";



# Example input:
#
# aampumakenttä	N	skytefelt


#Target output:
#
#   <e src="yr">
#      <lg>
#         <l pos="N">aampumakenttä</l>
#      </lg>
#      <mg>
#         <tg>
#            <t pos="N" gen="x">skytefelt</t>
#         </tg>
#      </mg>
#   </e>
#

