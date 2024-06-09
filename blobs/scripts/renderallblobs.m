function renderallblobs()

	settings.noise = 0.001;

	warning('OFF','Images:im2bw:binaryInput');

	outdr = outputdir('rendered');

	base = fullfile('..','data');

	lnames = {'doge1', 'ennis1', 'galileo1', 'grace1', 'hallstatt1', ...
	'pisa1', 'rnl1', 'tunnel1', 'uffizi1', 'window1'};

	for i = 1 : 10
		bname = sprintf('blob%02d_n.png',i);
		bpath = fullfile(base,bname);

		for j = 1 : 10
			lname = lnames{j};

			L = getlights(lname);

			[dr,nm,ex] = fileparts(bpath);
			basename = nm(1:end-2);
			btype = nm(end-1:end);

			mpath = fullfile(dr,[basename '_m.png']);
			msk = im2bw(imread(mpath));


			nrm = 2*im2double(imread(bpath))-1;
			im = shadeNormals(nrm, msk, L);

			im = im + settings.noise*randn(size(im));
			im = min(max(im,0),1);

			imname = sprintf('im_b%02d_l%02d.png',i,j);
			imwrite(im2uint16(im),fullfile(outdr,imname));
		end
	end
	
end




%
%
%
function name = outputdir(base)

	if ~exist('base','var')
		base = 'out';
	end

	name = sprintf('%s%02d',base,1);
	i = 2;
	while exist(name,'dir')
		name = sprintf('%s%02d',base,i);
		i = i + 1;
	end

	mkdir(name);
end

