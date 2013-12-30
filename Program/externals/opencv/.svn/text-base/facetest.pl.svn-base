#!/usr/bin/perl -w
#------------------------------------------------------------------------------
# File:         facetest.pl
#
# Syntax:       facetest.pl [MAKE|DIR|FILE]...
#
# Description:  test face detection/recognition decoding
#
# Revisions:    2011/02/26 - P. Harvey created
#               2011/03/27 - PH Restructured to provide FaceList() function
#                            and added support for more makes
#
# Face Colors:  Red/Blue - basic face area from newer/older format metadata
#               Green    - primary face(s)?
#               Orange   - recognized faces
#
# Notes:      - requires imagemagick 'convert' to be installed
#             - draws rectangles around faces and writes resized output images
#             - output images are written to 'tmp' directory
#             - defaults to input directory of '../testpics/facedetect/Olympus'
#             - processes only JPG images
#------------------------------------------------------------------------------
use strict;

BEGIN { unshift @INC, 'lib' }
use Image::ExifTool;

sub FaceList($$);   # prototype for the subroutine that does all of the hard work

# configurable parameters
my $resize = 640;   # maximum width of rescaled images
my $dstdir = 'tmp'; # destination directory for output images

my @files = @ARGV;
@files or push @files, '../testpics/facedetect/Olympus';
my $exifTool = new Image::ExifTool;

mkdir $dstdir;      # make sure destination directory exists

my $file;
foreach $file (@files) {
    unless (-e $file) {
        my $f = "../testpics/facedetect/$file";
        unless (-e $f) {
            warn("Can't open $file\n");
            next;
        }
        $file = $f;
    }
    if (-d $file) {
        # read all files in directory (recursively)
        opendir DIR, $file or warn("Error opening $file\n"), next;
        my @f = readdir DIR;
        closedir DIR;
        foreach (@f) {
            next if /^\./;
            push @files, "$file/$_";
        }
        next;
    }
    next unless $file =~ /\.jpe?g$/i; # process only JPEG images
        
    print "==== $file ";
    my $info = $exifTool->ImageInfo($file);
    
    # get the list of face information hashes
    my $faceList = FaceList($exifTool, $info);

    unless (ref $faceList) {
        print "[no face information]\n";
        warn "$faceList\n" if $faceList;
        next;
    }
    print "[$$info{Make}]\n";

    my ($width, $height) = @$info{'ImageWidth','ImageHeight'};
    my $aspect = $height / $width;
    # calculate dimensions for a resized image with a max width of $resize pixels
    my ($rw, $rh);
    if ($aspect < 1) {
        ($rw, $rh) = ($resize, int($resize * $aspect + 0.5));
    } else {
        ($rw, $rh) = (int($resize / $aspect + 0.5), $resize);
    }
    my @s = ($rw,$rh,$rw,$rh);  # scaling factors for face coordinates

    # initialize 'convert' command with default drawing parameters
    my $cmd = "convert '$file' -fill none -strokewidth 2 -resize ${rw}x$rh";

    my $index = -1;
    foreach my $faceInfo (@$faceList) {
        # set the rectangle colour
        my $idx = $$faceInfo{Type} || 0;
        unless ($idx == $index) {
            $index = $idx;
            $idx = 2 if $idx > 3;
            $cmd .= ' -stroke ' . ['red','green','blue','orange']->[$idx];
        }
        # scale the face rectangle to the coordinates of the resized image
        my @p;
        for (my $i=0; $i<4; ++$i) {
            $p[$i] = int($$faceInfo{Position}[$i] * $s[$i] + 0.5);
        }
        # draw the face rectangle
        $cmd .= " -draw 'rectangle $p[0],$p[1] $p[2],$p[3]'";

        if (defined $$faceInfo{Rotation}) {
            # draw the face orientation
            my $ang = $$faceInfo{Rotation} * 3.14159 / 180;  # convert to radians
            my ($cx, $cy) = (($p[0]+$p[2])/2, ($p[1]+$p[3])/2);
            my ($w, $h) = (abs($p[2]-$p[0]), abs($p[3]-$p[1]));
            my ($x, $y) = (int(($cx+$w/2*sin($ang))*10)/10, int(($cy-$h/2*cos($ang))*10)/10);
            $cmd .= " -draw \"path 'M $cx,$cy L $x,$y'\"";
        }
    }
    $index > -1 or print("No face\n"), next;

    # add destination filename to command
    my $name = $file;
    $name =~ s/.*\///; # remove directory name
    $cmd .= " '$dstdir/$name'";

    # resize the image and draw the face positions
    print "$cmd\n";
    system $cmd;
}

#------------------------------------------------------------------------------
# check to see if all specified tags were found
# Inputs: 0) tag info hash, 1) message to return, 2-N) tag names
# Returns: true if specified tags exist
sub Found($$@)
{
    local $_;
    my $info = $_[0];
    foreach (@_[2..$#_]) {
        next if defined $$info{$_};
        $_[1] = "Missing $_";
        return 0;
    }
    return 1;
}

#------------------------------------------------------------------------------
# Get margines and size of cropped image area in face detect frame
# Inputs: 0/1) face detect frame width/height
#         2) aspect ratio of original image (must be < 1)
# Returns: 0/1) X/Y cropped border size
#          2/3) width/height of cropped image
sub GetCropArea($$$)
{
    my ($fw, $fh, $aspect) = @_;
    my $crop_w = $fw;
    my $crop_h = $fw * $aspect;
    if ($crop_h > $fh) {
        $crop_w = $fh / $aspect;
        $crop_h = $fh;
    }
    my ($crop_x, $crop_y) = (($fw - $crop_w) / 2, ($fh - $crop_h) / 2);
    return ($crop_x, $crop_y, $crop_w, $crop_h);
}

#------------------------------------------------------------------------------
# Return normalized face information from tags extracted by ExifTool
# Inputs: 0) ExifTool object reference
#         1) image information hash reference (from call to ImageInfo)
# Returns: undef if there is no face-detect information, or
#          error string if there there were no faces or there was an error, or
#          reference to array of face information hashes on success
# Face information hash elements:
#   Position - left,top,right,bottom coordinates of face as a fraction of image size
#   Rotation - [optional] CW rotation angle of face in degrees
#   Type     - [optional] type of face information:
#                         0=normal, 1=primary, 2=old models, 3=recognized
#   Name     - [optional] face name if recognized (FujiFilm, Panasonic)
#   Age      - [optional] age of person (FujiFilm, Panasonic)
#   Category - [optional] camera category for this face (FujiFilm)
sub FaceList($$)
{
    local $_;
    my ($exifTool, $info) = @_;
    my ($tag, $make, @faceList, $wasRotated, $msg, $i);
    
    return undef unless $$info{ImageWidth} and $$info{ImageHeight};

    my ($width, $height) = @$info{'ImageWidth','ImageHeight'};
    # all face detect coordinates are in unrotated image
    if ($height > $width) {
        # image was probably rotated, but face detect coordinates are always
        # given for the unrotated image, so assume that width is the long dimension
        my $tmp = $width;
        $width = $height;
        $height = $tmp;
        $wasRotated = 1;
    }
    my $aspect = $height / $width;
    my ($fw, $fh);  # face detect frame width/height
    my ($sx, $sy);  # x/y scaling factors

    # get the ExifTool manufacturer group name
    foreach $tag ('FacesDetected', 'ValidAFPoints') {
        next unless defined $$info{$tag};
        $make = $exifTool->GetGroup($tag, 1);
        last;
    }
    my $model = $$info{Model} || '';
    $make or return 'Unrecognized face information!';
#
# unfortunately each manufacturer has its own way of storing face detection
# information, so we must handle them all differently...
#
    if ($make eq 'Sony') {

       return $msg unless Found($info, $msg, 'FacesDetected', 'Face1Position');
        # calculate scaling factors for face detect area coordinates
        ($sx, $sy) = (1/$width, 1/$height);
        for ($i=1; ; ++$i) {
            my $tag = "Face${i}Position";
            last unless $$info{$tag};
            my @a = split ' ', $$info{$tag};
            last unless @a >= 4;
            my ($x1, $y1) = ($a[1]*$sx, $a[0]*$sy);
            my ($x2, $y2) = ($x1+$a[3]*$sx, $y1+$a[2]*$sy);
            push @faceList, { Position => [$x1, $y1, $x2, $y2] };
        }

    } elsif ($make eq 'FujiFilm') {

        return $msg unless Found($info, $msg, 'FacesDetected', 'FacePositions');
        my $n = $$info{FacesDetected} or return 'No faces';
        my @a = split ' ', $$info{FacePositions};
        ($sx, $sy) = (1/$width, 1/$height);
        for ($i=0; $i<$n; ++$i) {
            my ($x1, $y1) = ($a[$i*4]*$sx, $a[$i*4+1]*$sy);
            my ($x2, $y2) = ($a[$i*4+2]*$sx, $a[$i*4+3]*$sy);
            my $faceInfo = { Position => [$x1, $y1, $x2, $y2] };
            push @faceList, $faceInfo;
            my $name = $$info{"Face${i}Name"};
            next unless defined $name;
            $$faceInfo{Type} = 3; # recognized face
            $$faceInfo{Name} = $name;
            $$faceInfo{Category} = $$info{"Face${i}Category"};
            # calculate age
            my $bday = $$info{"Face${i}Birthday"} or next;
            my $date = $$info{DateTimeOriginal} || $$info{CreateDate} or next;
            my @t1 = $bday =~ /\d+/g;
            my @t2 = $date =~ /\d+/g;
            push @t1, 0 while @t1 < 6;  # pad with zeros
            push @t2, 0 while @t1 < 6;
            my $borrow = 0;
            my ($j, @age);
            for ($j=5; $j>=0; --$j) {
                $age[$j] = $t2[$j] - $t1[$j] - $borrow;
                $age[$j] >= 0 and $borrow = 0, next;
                last unless $j;
                # handle borrow in subtraction
                $borrow = 1;
                my $add = [0, 12, 0, 24, 60, 60]->[$j];
                $add and $age[$j] += $add, next;
                # borrow days from the month before
                my ($m, $y) = ($t2[1]-1, $t2[0]);
                $age[$j] += [31,31,28,31,30,31,30,31,31,30,31,30]->[$m];
                # handle leap years if month is February
                $age[$j] += 1 if $m==2 and $y % 4 and ($y % 100 or not $y % 400);
            }
            $$faceInfo{Age} = sprintf('%.4d:%.2d:%.2d %.2d:%.2d:%.2d', @age);
        }

    } elsif ($make eq 'Nikon') {

        return $msg unless Found($info, $msg, 'FacesDetected', 'FaceDetectFrameSize', 'Face1Position');
        ($fw,$fh) = split ' ', $$info{FaceDetectFrameSize};
        # (note: have seen crazy $fh for S550, so scale Y by same factor as X)
        ($sx,$sy) = (1/$fw, 1/$fh);
        for ($i=1; ; ++$i) {
            my $val = $$info{"Face${i}Position"} or last;
            my @a = split ' ', $val;
            # (have seen high bit set in a S550 sample, so reset it just in case)
            my ($x1,$y1) = (($a[0]&0x7fff)*$sx, ($a[1]&0x7fff)*$sy);
            my ($x2,$y2) = ($x1+$a[2]*$sx, $y1+$a[3]*$sy);
            push @faceList, { Position => [$x1, $y1, $x2, $y2] };
        }

    } elsif ($make eq 'Panasonic') {

        return $msg unless Found($info, $msg, 'FacesDetected', 'Face1Position');
        # face detect frame is 320 pixels wide unless aspect ratio is less than 3/4
        if ($aspect <= 3/4) {
            ($fw, $fh) = (320, 320 * $aspect);
        } else {
            ($fw, $fh) = (240 / $aspect, 240);
        }
        ($sx, $sy) = (1/$fw, 1/$fh);
        my $type;
        for ($type=0; $type<2; ++$type) {
            my $pre = $type ? 'Recognized' : '';
            for ($i=1; ; ++$i) {
                my $val = $$info{"${pre}Face${i}Position"} or last;
                my @a = split ' ', $val;
                my ($x1,$y1) = (($a[0]-$a[2]/2)*$sx, ($a[1]-$a[3]/2)*$sy);
                my ($x2,$y2) = ($x1+$a[2]*$sx, $y1+$a[3]*$sy);
                my $faceInfo = { Position => [$x1, $y1, $x2, $y2] };
                push @faceList, $faceInfo;
                next unless $type;
                $$faceInfo{Type} = 3;  # use index 3 for recognized faces
                $$faceInfo{Name} = $$info{"RecognizedFace${i}Name"};
                $$faceInfo{Age} = $$info{"RecognizedFace${i}Age"};
            }
        }

    } elsif ($make eq 'Pentax') {

        return $msg unless Found($info, $msg, 'FacesDetected', 'Face1Position');
        my $n = $$info{FacesDetected};
        $n or return 'No faces';
        ($sx,$sy) = (1/$width, 1/$height);
        for ($i=1; $i<=$n; ++$i) {
            my $val = $$info{"Face${i}Position"} or last;
            my ($x,$y) = split ' ', $val;
            $val = $$info{"Face${i}Size"} or last;
            my ($w,$h) = split ' ', $val;
            my ($x1,$y1) = (($x-$w/2)*$sx, ($y-$h/2)*$sy);
            my ($x2,$y2) = ($x1+$w*$sx, $y1+$h*$sy);
            push @faceList, { Position => [$x1, $y1, $x2, $y2] };
        }
        if ($$info{'FacePosition'}) {
            my ($x,$y) = split ' ', $$info{FacePosition};
            my $w = 100; # (just pull a number for the face size out of thin air)
            my ($x1,$y1) = ($x/100-$w/2, $y/100-$w/2);
            my ($x2,$y2) = ($x1+$w, $y1+$w);
            # set the Type for the primary face
            push @faceList, { Position => [$x1, $y1, $x2, $y2], Type => 1 };
        }

    } elsif ($make eq 'Sanyo') {

        return $msg unless Found($info, $msg, 'FacesDetected', 'FacePosition');
        # face detect frame is 640 pixels wide
        ($fw, $fh) = (640, 640 * $aspect);
        ($sx, $sy) = (1/$fw, 1/$fh);
        my $val = $$info{"FacePosition"} or last;
        my @a = split ' ', $val;
        my ($x1,$y1) = ($a[0]*$sx, $a[1]*$sy);
        my ($x2,$y2) = ($a[2]*$sx, $a[3]*$sy);
        push @faceList, { Position => [$x1, $y1, $x2, $y2] };

    } elsif ($make eq 'Casio') {

        return $msg unless Found($info, $msg, 'FacesDetected', 'FaceDetectFrameSize', 'Face1Position');
        # extract face orientation if available
        my $rot;
        $rot = $$info{FaceOrientation} =~ /(\d+)/ ? $1 : 0 if $$info{FaceOrientation};
        ($fw, $fh) = split ' ', $$info{FaceDetectFrameSize};
        my ($crop_x, $crop_y, $crop_w, $crop_h) = GetCropArea($fw, $fh, $aspect);
        ($sx, $sy) = (1/$crop_w, 1/$crop_h);
        for ($i=1; ; ++$i) {
            my $val = $$info{"Face${i}Position"} or last;
            my @a = split ' ', $val;
            my ($x1,$y1) = (($a[0]-$crop_x)*$sx, ($a[1]-$crop_y)*$sy);
            my ($x2,$y2) = (($a[2]-$crop_x)*$sx, ($a[3]-$crop_y)*$sy);
            my $faceInfo = { Position => [$x1, $y1, $x2, $y2] };
            $$faceInfo{Rotation} = $rot if defined $rot;
            push @faceList, $faceInfo;
        }

    } elsif ($make eq 'Ricoh') {

        return $msg unless Found($info, $msg, 'FacesDetected', 'FaceDetectFrameSize', 'Face1Position');
        ($fw, $fh) = split ' ', $$info{FaceDetectFrameSize};
        my ($sx, $sy) = (1/$fw, 1/$fh);
        for ($i=1; ; ++$i) {
            my $val = $$info{"Face${i}Position"} or last;
            my ($x,$y,$w,$h) = split ' ', $val;
            my ($x1,$y1) = ($x/$fw, $y*$sy);
            my ($x2,$y2) = (($x+$w)*$sx, ($y+$h)*$sy);
            push @faceList, { Position => [$x1, $y1, $x2, $y2] };
        }

    } elsif ($make eq 'Canon') {

        # older models store face detect information
        if ($$info{FacesDetected} and $$info{FaceDetectFrameSize}) {
            return 'No faces' unless $$info{FacesDetected};
            ($fw, $fh) = split ' ', $$info{FaceDetectFrameSize};
            $fw or ($fw,$fh) = (320,240);
            ($sx,$sy) = (1/$fw, 1/$fh);
            my $facewid = $$info{FaceWidth} || 35;
            for ($i=1; ; ++$i) {
                my $val = $$info{"Face${i}Position"} or last;
                my @a = split ' ', $val;
                my ($x1,$y1) = (($a[0]+$fw/2-$facewid)*$sx, ($a[1]+$fh/2-$facewid)*$sy);
                my ($x2,$y2) = ($x1+$facewid*2*$sx, $y1+$facewid*2*$sy);
                # set Type to 2 for older Canon face-detect information
                push @faceList, { Position => [$x1, $y1, $x2, $y2], Type => 2 };
            }
        } else { # newer models use AF points
            return $msg unless Found($info, $msg, 'ValidAFPoints', 'AFImageWidth', 'AFImageHeight',
                              'AFAreaXPositions', 'AFAreaYPositions', 'PrimaryAFPoint');
            # test for face detect mode
            unless ($$info{AFAreaMode} and $$info{AFAreaMode} =~ /Face/) {
                return 'Face detect off';
            }
            my ($width, $height) = @$info{'AFImageWidth', 'AFImageHeight'};
            my @x = split ' ', $$info{AFAreaXPositions};
            my @y = split ' ', $$info{AFAreaYPositions};
            # sometimes widths are stored separately for each AF area
            my (@w, @h);
            if ($$info{AFAreaWidths}) {
                @w = split ' ', $$info{AFAreaWidths};
                @h = split ' ', $$info{AFAreaHeights};
            } elsif ($$info{AFAreaWidth}) {
                @w = ($$info{AFAreaWidth}) x (scalar @x);
                @h = ($$info{AFAreaHeight}) x (scalar @x);
            } else {
                return 'No AF area size';
            }
            # convert to positive coordinates
            $_ += $width/2 foreach @x;
            $_ += $height/2 foreach @y;
            # EOS models have Y flipped
            if ($model =~ /EOS/) {
                $_ = $height - $_ foreach @y;
            }
            # calculate scaling factors for AF area coordinates
            ($sx,$sy) = (1/$width, 1/$height);
            for ($i=0; $i<$$info{ValidAFPoints}; ++$i) {
                my ($x1,$y1) = (($x[$i]-$w[$i]/2)*$sx, ($y[$i]-$h[$i]/2)*$sy);
                my ($x2,$y2) = ($x1+$w[$i]*$sx, $y1+$h[$i]*$sy);
                push @faceList, { Position => [$x1, $y1, $x2, $y2] };
            }
        }

    } elsif ($make eq 'Olympus') {

        # Olympus stores 1 or 2 (or maybe more in the future) sets of face-detect data.
        # I'm not sure why, but the 2nd set (Type 1) seems to be more accurate.
        return $msg unless Found($info, $msg, 'FacesDetected', 'FaceDetectArea');
        my @f = split ' ', $$info{FacesDetected};
        return 'No faces' unless $f[0] or $f[1];
        my @a = split ' ', ${$$info{FaceDetectArea}};
        my (@m, $type, $index);
        if ($$info{MaxFaces}) {
            @m = split ' ', $$info{MaxFaces};
            $type = 'new';
            $index = 0;
        } else {
            push @m, 0;
            $index = 2; # information from older models
        }

        # get face detect frame size
        if ($$info{FaceDetectFrameSize} and
            $$info{FaceDetectFrameSize} =~ /^(\d+) (\d+)/)
        {
            ($fw, $fh) = ($1, $2);
        } else {
            ($fw, $fh) = (240, 180);  # empirically determined for older models
        }

        # get width/height of largest resized image that fits into face detect frame
        my ($crop_w, $crop_h, $crop_x, $crop_y);
        if ($$info{FaceDetectFrameCrop} and
            $$info{FaceDetectFrameCrop} =~ /^(\d+) (\d+) (\d+) (\d+)/)
        {
            ($crop_x, $crop_y, $crop_w, $crop_h) = ($1, $2, $3, $4);
        } else {
            ($crop_x, $crop_y, $crop_w, $crop_h) = GetCropArea($fw, $fh, $aspect);
        }
        ($sx, $sy) = (1/$crop_w, 1/$crop_h);
        my $rot = 90; # default rotation angle to landscape
        my ($orient, $max);
        $orient = $1 if $$info{Orientation} and $$info{Orientation} =~ /(\d+)/;
        my $pos = 0;
        foreach $max (@m) {
            my $faces = shift @f;
            my $face;
            for ($face=0; $face<$faces; ++$face) {
                last if $pos + 4 > scalar @a;
                my $n = $pos + $face * ($type ? 4 : 8);
                my ($x1,$y1,$x2,$y2,$xc,$yc,$rotation);
                if ($type) {
                    my ($x,$y,$w,$r) = @a[$n..($n+3)];
                    if (defined $orient) {
                        # the angle depends on orientation for some models (doh!)
                        $r -= $orient if $model eq 'u-7050';
                    } else {
                        # rotate by 270 if any face orientation is 270 degrees
                        $rot = 270 if $r == 270;
                        # again, angle depends on orientation for some models
                        $r -= $rot if $wasRotated and $model =~ /^FE4030/;
                    }
                    $rotation = $r;
                    $rotation += 360 if $rotation < 0;
                    my $hx = $w * $sx / 2;
                    my $hy = $w * $sy / 2;
                    # adjust coordinates for cropped border and normalize
                    $xc = ($x - $crop_x) * $sx;
                    $yc = ($y - $crop_y) * $sy;
                    ($x1, $y1) = ($xc - $hx, $yc - $hy);
                    ($x2, $y2) = ($x1 + $w * $sx, $y1 + $w * $sy);
                } else {
                    # adjust coordinates for cropped image
                    for ($i=$n; $i<$n+8; $i+=2) {
                        $a[$i] = ($a[$i] - $crop_x) * $sx;
                        $a[$i+1] = ($a[$i+1] - $crop_y) * $sy;
                    }
                    my ($x3,$y3,$x4,$y4);
                    ($x1,$y1,$x2,$y2,$x3,$y3,$x4,$y4) = @a[$n..($n+7)];
                    if ($y1 == $y2) {
                        $rotation = $x1 < $x2 ? 0 : 180;
                    } else {
                        $rotation = $y1 < $y2 ? 90 : 270;
                    }
                    $x2 = $x3 if $x2 == $x1;
                    $y2 = $y3 if $y2 == $y1;
                }
                # draw the face rectangle and line pointing to the top of the face
                push @faceList, {
                    Position => [$x1, $y1, $x2, $y2],
                    Rotation => $rotation,
                    Type => $index,
                };
            }
            $pos += $max * 4;
            ++$index;
        }

    } else {

        return "Sorry, $make images not yet supported";

    }

    # finally, rotate face coordinates if image was rotated
    if ($wasRotated) {
        my $rot = 270;
        my $faceInfo;
        foreach $faceInfo (@faceList) {
            next unless defined $$faceInfo{Rotation};
            $rot = $$faceInfo{Rotation} < 180 ? 90 : 270;
            last;
        }
        # rotate face coordinates
        foreach $faceInfo (@faceList) {
            my $p = $$faceInfo{Position};
            if ($rot == 90) {
                @$p = ($$p[1], 1-$$p[0], $$p[3], 1-$$p[2]);
            } else {
                @$p = (1-$$p[1], $$p[0], 1-$$p[3], $$p[2]);
            }
            next unless defined $$faceInfo{Rotation};
            $$faceInfo{Rotation} -= $rot;
            $$faceInfo{Rotation} += 360 if $$faceInfo{Rotation} < 0;
        }
    }
    return \@faceList;
}

# end
