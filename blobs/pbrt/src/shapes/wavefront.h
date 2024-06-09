
#ifndef PBRT_SHAPES_WAVEFRONT_H
#define PBRT_SHAPES_WAVEFRONT_H

#include "shape.h"

class Wavefront : public Shape {
	public:
		Wavefront(const char* filename, const Transform *o2w, 
				const Transform *w2o, bool reverseOrientation);
		~Wavefront() {
			if (vertexIndex) delete[] vertexIndex;
			if (p) delete[] p;
			if (n) delete[] n;
			if (uvs) delete[] uvs;
		}
		
		BBox ObjectBound() const;
		BBox WorldBound() const;
		bool CanIntersect() const { return false; }
		void Refine(vector<Reference<Shape> > &refined) const;

	private:
		void MergeIndicies(vector<Point> &points, vector<Normal> &normals, vector<float> &uvVec,
							vector<int> &vIndex, vector<int> &normalIndex, vector<int> &uvIndex);
		int ntris, nverts;
		int nVerticesTotal;
		int *vertexIndex;
		Point *p;
		Normal *n;
		float *uvs;
};

Wavefront *CreateWavefrontShape(const Transform *o2w, const Transform *w2o,
        bool reverseOrientation, const ParamSet &params);

#endif

