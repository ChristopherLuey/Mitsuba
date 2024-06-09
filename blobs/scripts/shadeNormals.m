%shadeNormals
%
%	Apply a lighting function to normals
%
% -Usage-
%	sim = shadeNormals(nrm, mask, L)
%
% -Inputs-
%	nrm
%	mask
%	L
%
% -Outputs-
%	sim
%
% Last Modified: 10/28/2010
function sim = shadeNormals(nrm, mask, L)

	[ydim,xdim,zdim] = size(nrm);
	nL = numel(L);
	sim = zeros(ydim,xdim,nL);

	tempnrm = reshape(nrm,[ydim*xdim 3])';
	for c = 1 : nL
		sig = sum(tempnrm.*(L(c).A*tempnrm)) + L(c).b'*tempnrm + L(c).c;
		tempim = reshape(sig,[ydim xdim]);
		tempim(~mask) = 0.5;
		
		sim(:,:,c) = tempim;
	end
	
end

