#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
"""PdfFit class for fitting pdf data to a model."""
import pdffit2

class PdfFit(object):
    """Create PdfFit object."""
    import sys

    # constants and enumerators from pdffit.h:
    # selection of all atoms
    selalias = { 'ALL' : -1 }
    # constraint type identifiers
    FCON = { 'USER' : 0, 'IDENT' : 1, 'FCOMP' : 2, 'FSQR' : 3 }
    # scattering type identifiers
    Sctp = { 'X' : 0, 'N' : 1 }

    def _exportAll(self, namespace):
        """ _exportAll(self, namespace) --> Export all 'public' class methods
            into namespace.  
        
        This function allows for a module-level PdfFit object which doesn't have
        to be referenced when calling a method. This function makes old (python)
        scripts compatible with this class. At the top of the script, create a
        pdffit object, and then call this method. Usually, namespace =
        sys.modules[__name__].__dict__.

       
        """
        # string aliases (var = "var")
        for a in self.selalias.keys() + self.FCON.keys() + self.Sctp.keys():
            exec("%s = %r" % (a, a), namespace)
        public = [ a for a in dir(self) if "__" not in a and a not in 
                ["_handle", "_exportAll", "selalias", "FCON", "Sctp" ] ]
        import sys
        for funcname in public:
            namespace[funcname] = getattr(self, funcname)
        return


    def read_struct(self, struct):
        """read_struct(struct) --> Read structure from file into memory.
        
        struct  -- name of file from which to read structure 
        
        Raises: 
            pdffit2.calculationError when a lattice cannot be created from the
            given structure
            pdffit2.structureError when a structure file is malformed
            IOError when the file cannot be read from the disk
        """
        pdffit2.read_struct(self._handle, struct)
        self.stru_files.append(struct)
        return


    def read_struct_string(self, struct, name = ""):
        """read_struct_string(struct, name = "") --> Read structure from
        a string into memory.
        
        struct  -- string containing the contents of the structure file
        name    -- tag with which to label structure
        
        Raises: 
            pdffit2.calculationError when a lattice cannot be created from the
            given structure
            pdffit2.structureError when a structure file is malformed
        """
        pdffit2.read_struct_string(self._handle, struct)
        self.stru_files.append(name)
        return


    def read_data(self, data, stype, qmax, sigmaq):
        """read_data(data, stype, qmax, sigmaq) --> Read pdf data from file into
        memory.

        data    -- name of file from which to read data
        stype   -- 'X' (xray) or 'N' (neutron)
        qmax    -- Q-value cutoff used in PDF calculation.
                   Use qmax=0 to neglect termination ripples.
        sigmaq  -- instrumental Q-resolution factor
        
        Raises: IOError when the file cannot be read from disk
        """
        pdffit2.read_data(self._handle, data, self.Sctp[stype], qmax, sigmaq)
        self.data_files.append(data)
        if self.data_server:
            self.data_server.setDataDescriptor(data)
        return


    def read_data_string(self, data, stype, qmax, sigmaq, name = ""):
        """read_data_string(data, stype, qmax, sigmaq, name = "") --> Read
        pdf data from a string into memory.

        data    -- string containing the contents of the data file
        stype   -- 'X' (xray) or 'N' (neutron)
        qmax    -- Q-value cutoff used in PDF calculation.
                   Use qmax=0 to neglect termination ripples.
        sigmaq  -- instrumental Q-resolution factor
        name    -- tag with which to label data
        """
        pdffit2.read_data_string(self._handle, data, self.Sctp[stype], qmax,
                sigmaq, name)
        name = data
        self.data_files.append(name)
        if self.data_server:
            self.data_server.setDataDescriptor(name)
        return


    def read_data_lists(self, stype, qmax, sigmaq, r_data, Gr_data, 
            dGr_data = None, name = "list"):
        """read_data_lists(stype, qmax, sigmaq, r_data, Gr_data, dGr_data =
        None, name = "list") --> Read pdf data into memory from lists. 
        
        All lists must be of the same length.
        stype       -- 'X' (xray) or 'N' (neutron)
        qmax        -- Q-value cutoff used in PDF calculation.
                       Use qmax=0 to neglect termination ripples.
        sigmaq      -- instrumental Q-resolution factor
        r_data      -- list of r-values
        Gr_data     -- list of G(r) values
        dGr_data    -- list of G(r) uncertainty values
        name        -- tag with which to label data
        
        Raises: ValueError when the data lists are of different length
        """
        pdffit2.read_data_arrays(self._handle, self.Sctp[stype], qmax, sigmaq,
                r_data, Gr_data, dGr_data, name)
        self.data_files.append(name)
        return


    def pdfrange(self, iset, rmin, rmax):
        """pdfrange(iset, rmin, rmax) --> Set the range of the fit.
        
        iset    -- data set to consider
        rmin    -- minimum r-value of fit
        rmax    -- maximum r-value of fit
        
        Raises: ValueError for bad input values
        """
        pdffit2.pdfrange(self._handle, iset, rmin, rmax)
        return


    def reset(self):
        """reset() --> Clear all stored fit, structure, and parameter data."""
        self.stru_files = []
        self.data_files = []
        pdffit2.reset(self._handle);
        return


    def alloc(self, stype, qmax, sigmaq, rmin, rmax, bin):
        """alloc(stype, qmax, sigmaq, rmin, rmax, bin) --> Allocate space for a 
        PDF calculation. 
        
        The structure from which to calculate the PDF must first be imported with
        the read_struct() or read_struct_string() method.
        stype   -- 'X' (xray) or 'N' (neutron)
        qmax    -- Q-value cutoff used in PDF calculation.
                   Use qmax=0 to neglect termination ripples.
        sigmaq  -- instrumental Q-resolution factor
        rmin    -- minimum r-value of calculation
        rmax    -- maximum r-value of calculation
        bin     -- number of data points in calculation
        
        Raises: 
            ValueError for bad input values
            pdffit.unassignedError when no structure has been loaded
        """
        pdffit2.alloc(self._handle, self.Sctp[stype], qmax, sigmaq, rmin, 
                rmax, bin)
        return


    def calc(self):
        """calc() --> Calculate the PDF of the imported structure.
        
        Space for the calculation must first be allocated with the alloc()
        method.
        
        Raises: 
            pdffit2.calculationError when allocated space cannot
            accomodate calculation
            pdffit.unassignedError when space for calculation has not been
            allocated
        """
        pdffit2.calc(self._handle)
        return


    def refine(self, toler = 0.00000001):
        """refine(toler = 0.00000001) --> Fit the theory to the imported data.

        toler   --  tolerance of the fit
        
        Raises: 
            pdffit2.calculationError when the model pdf cannot be calculated
            pdffit2.constraintError when refinement fails due to bad
            constraint
            pdffit2.unassigedError when a constraint used but never initialized
            using setpar()
        """
        step = 0
        finished = 0
        while not finished:
            finished = pdffit2.refine_step(self._handle, toler)
            step += 1
            if self.data_server: 
                import time
                self.data_server.update(self, step, finished)
                time.sleep(0.1)
        return


    def refine_step(self, toler = 0.00000001):
        """refine_step(toler = 0.00000001) --> Run a single step of the fit.
        
        toler   --  tolerance of the fit

        Raises: 
            pdffit2.calculationError when the model pdf cannot be calculated
            pdffit2.constraintError when refinement fails due to bad
            constraint
            pdffit2.unassigedError when a constraint used but never initialized
            using setpar()

        Returns: 1 (0) if refinement is (is not) finished
        """
        self.finished = pdffit2.refine_step(self._handle, toler)
        return self.finished


    def save_pdf(self, iset, fname):
        """save_pdf(iset, fname) --> Save calculated or fitted PDF to file.
        
        iset    -- data set to save
        
        Raises: 
            IOError if file cannot be saved
            pdffit2.unassignedError if the data set is undefined
        """
        pdffit2.save_pdf(self._handle, iset, fname)
        return


    def save_pdf_string(self, iset):
        """save_pdf_string(iset) --> Save calculated or fitted PDF to string.
        
        iset    -- data set to save
        
        Raises: 
            pdffit2.unassignedError if the data set is undefined

        Returns: string containing contents of save file
        """
        pdffilestring = pdffit2.save_pdf(self._handle, iset, "")
        return pdffilestring


    def save_dif(self, iset, fname):
        """save_dif(iset, fname) --> Save data and fitted PDF difference to
        file.
        
        iset    -- data set to save
        
        Raises: 
            IOError if file cannot be saved
            pdffit2.unassignedError if the data set is undefined
        """
        pdffit2.save_dif(self._handle, iset, fname)
        return


    def save_dif_string(self, iset):
        """save_dif_string(iset) --> Save data and fitted PDF difference to
        string.
        
        iset    -- data set to save
        
        Raises: 
            pdffit2.unassignedError if the data set is undefined
        
        Returns: string containing contents of save file
        """
        diffilestring = pdffit2.save_dif(self._handle, iset, "")
        return diffilestring


    def save_res(self, fname):
        """save_res(fname) --> Save fit-specific data to file.
        
        Raises: 
            IOError if file cannot be saved
            pdffit2.unassignedError if there is no refinement data to save 
        """
        pdffit2.save_res(self._handle, fname)
        return
    

    def save_res_string(self):
        """save_res_string() --> Save fit-specific data to a string.
        
        Raises: 
            pdffit2.unassignedError if there is no refinement data to save 
        
        Returns: string containing contents of save file
        """
        resfilestring = pdffit2.save_res(self._handle, "")
        return resfilestring
    

    def save_struct(self, ip, fname):
        """save_struct(ip, fname) --> Save structure resulting from fit
        to file.
        
        ip    -- phase to save
        
        Raises: 
            IOError if file cannot be saved
            pdffit2.unassignedError if the data set is undefined
        """
        pdffit2.save_struct(self._handle, ip, fname)
        return


    def save_struct_string(self, ip):
        """save_struct(ip) --> Save structure resulting from fit to string.
        
        ip    -- phase to save
        
        Raises: 
            pdffit2.unassignedError if the data set is undefined
        
        Returns: string containing contents of save file
        """
        structfilestring = pdffit2.save_struct(self._handle, ip, "")
        return structfilestring


    def show_struct(self, ip):
        """show_struct(ip) --> Print structure resulting from fit.
        
        ip    -- phase to display
        
        Raises: pdffit2.unassignedError if the phase is undefined
        """
        pdffit2.show_struct(self._handle, ip)
        return


    def constrain(self, var, par, fcon=None):
        """constrain(var, par[, fcon]) --> Constrain a variable to a parameter.
        
        A variable can be constrained to a number or equation string. 
        var     -- variable to constrain, such as x(1)
        par     -- parameter which to constrain the variable. This can be
                   an integer or an equation string containing a reference
                   to another parameter. Equation strings use standard c++ 
                   syntax. The value of a constrained parameter is accessed 
                   as @p in an equation string, where p is the parameter.
                   e.g.
                   >>>  constrain(x(1), 1)
                   >>>  constrain(x(2), "0.5+@1")
        fcon    -- 'USER', 'IDENT', 'FCOMP', or 'FSQR'
                   this is an optional parameter, and I don't know how it is
                   used!
        
        Raises: 
            pdffit2.constraintError if a constraint is bad
            pdffit2.unassignedError if variable does not yet exist
            ValueError if variable index does not exist (e.g. lat(7))
        """
        import types
        var_ref = self.__getRef(var)
        if fcon:
            pdffit2.constrain_int(self._handle, var_ref, par, self.FCON[fcon])
        elif type(par) == types.StringType:
            pdffit2.constrain_str(self._handle, var_ref, par)
        else:
            pdffit2.constrain_int(self._handle, var_ref, par)
        return


    def setpar(self, par, val):
        """setpar(par, val) --> Set value of constrained parameter.
        
        val     --  Either a numerical value or a reference to a variable
        
        Raises: 
            pdffit2.unassignedError when variable is yet to be assigned
        """
        # people do not use parenthesis, e.g., "setpar(3, qsig)"
        # in such case val is a reference to PdfFit method
        import types
        if type(val) is types.MethodType:
            val = val()
        try:
            val = float(val)
            pdffit2.setpar_dbl(self._handle, par, val)
        except ValueError:
            var_ref = self.__getRef(val)
            pdffit2.setpar_RV(self._handle, par, var_ref) 
        return


    def setvar(self, var, val):
        """setvar(var, val) --> Set the value of a variable.
        
        Raises: 
            pdffit2.unassignedError if variable does not yet exist
            ValueError if variable index does not exist (e.g. lat(7))
        """
        var_ref = self.__getRef(var)
        pdffit2.setvar(self._handle, var_ref, val)
        return


    def getvar(self, var):
        """getvar(var) --> Get stored value of a variable.
        
        Raises: 
            pdffit2.unassignedError if variable does not yet exist
            ValueError if variable index does not exist (e.g. lat(7))
        """
        var_ref = self.__getRef(var)
        retval = pdffit2.getvar(self._handle, var_ref)
        return retval


    def getrw(self):
        """getrw() --> Get goodness of fit value, rw."""
        rw = pdffit2.getrw(self._handle)
        return rw


    def getR(self):
        """getR() --> Get r-points used in the fit. 
        
        This function should only be called after data has been loaded or
        calculated. Before a refinement, the list of r-points will reflect the
        data. Afterwords, they will reflect the fit range.
        
        Raises: pdffit2.unassignedError if no data exists
       
        Returns: List of equidistance r-points used in fit.
        """
        R = pdffit2.getR(self._handle)
        return R


    def getpdf_fit(self):
        """getpdf_fit() --> Get fitted PDF.
        
        This function should only be called after a refinement or refinement
        step has been done.
        
        Raises: pdffit2.unassignedError if no data exists 
       
        Returns: List of fitted points, equidistant in r.
        """
        pdfdata = pdffit2.getpdf_fit(self._handle)
        return pdfdata


    def getpdf_obs(self):
        """getpdf_obs() --> Get observed PDF.
        
        This function should only be called after data has been loaded or
        calculated. Before a refinement, the list of r-points will reflect the
        data. Afterwords, they will reflect the fit range.
        
        Raises: pdffit2.unassignedError if no data exists 
       
        Returns: List of data points, equidistant in r.
        """
        pdfdata = pdffit2.getpdf_obs(self._handle)
        return pdfdata


    def get_atoms(self):
        """get_atoms() --> Get atoms in the structure.
        
        This function should only be called after a structure has been loaded.
        
        Raises: pdffit2.unassignedError if no structure exists 
        
        Returns: List of atom names in structure.
        """
        atoms = pdffit2.get_atoms(self._handle)
        return atoms


    def get_xyz(self):
        """get_xyz() --> Get atom names and positions.
        
        This function should only be called after a structure has been loaded.
        
        Raises: pdffit2.unassignedError if no structure exists 
       
        Returns: List of (name, x, y, z) tuples.
        """
        num_atoms = self.num_atoms()
        atom_names = self.get_atoms()
        print atom_names
        atoms = []
        if num_atoms > 0:
            a = self.getvar(self.lat(1))
            b = self.getvar(self.lat(2))
            c = self.getvar(self.lat(3))
            for i in range(num_atoms):
                x_val = a*self.getvar(self.x(1+i))
                y_val = b*self.getvar(self.y(1+i))
                z_val = c*self.getvar(self.z(1+i))
                atoms.append((atom_names[i], x_val, y_val, z_val))
        return atoms


    def getpar(self, par):
        """getpar(par) --> Get value of parameter.
        
        Raises: ValueError if parameter does not exists 
        """
        return pdffit2.getpar(self._handle, par)


    def fixpar(self, par):
        """fixpar(par) --> Fix a parameter.
        
        Fixed parameters are not fitted in a refinement. Passed parameter
        can be 'ALL', in which case all parameters are fixed.

        Raises: pdffit.unassignedError when parameter has not been assigned
        """
        import types
        if type(par) in types.StringTypes and par.upper() in self.selalias:
            par = self.selalias[par.upper()]
        pdffit2.fixpar(self._handle, par)
        return


    def freepar(self, par):
        """freepar(par) --> Free a parameter. 
        
        Freed parameters are fitted in a refinement. Passed parameter
        can be 'ALL', in which case all parameters are freed.

        Raises: pdffit.unassignedError when parameter has not been assigned
        """
        import types
        if type(par) in types.StringTypes and par.upper() in self.selalias:
            par = self.selalias[par.upper()]
        pdffit2.freepar(self._handle, par)
        return


    def setphase(self, ip):
        """setphase(ip) --> Switch to phase ip.
        
        All parameters assigned after this method is called refer only to the
        current phase.
        
        Raises: pdffit.unassignedError when phase does not exist 
        """
        pdffit2.setphase(self._handle, ip)
        return


    def setdata(self, iset):
        """setdata(iset) --> Set the data in focus.
        
        Raises: pdffit.unassignedError when data set does not exist 
        """
        pdffit2.setdata(self._handle, iset)
        return


    def psel(self, ip):
        """psel(ip) --> Include phase ip in calculation of total PDF

        psel('ALL')     selects all phases for PDF calculation.
        
        Raises: pdffit2.unassignedError if selected phase does not exist
        """
        import types
        if type(ip) in types.StringTypes and ip.upper() in self.selalias:
            ip = self.selalias[ip.upper()]
        pdffit2.psel(self._handle, ip)
        return


    def pdesel(self, ip):
        """pdesel(ip) --> Exclude phase ip from calculation of total PDF.
        
        pdesel('ALL')   excludes all phases from PDF calculation.

        Raises: pdffit2.unassignedError if selected phase does not exist
        """
        import types
        if type(ip) in types.StringTypes and ip.upper() in self.selalias:
            ip = self.selalias[ip.upper()]
        pdffit2.pdesel(self._handle, ip)
        return


    def isel(self, iset, i):
        """isel(iset, i) --> Include atoms of type i from phase iset as first
        in pair distance evaluation.  Used for calculation of partial PDF.
        When i is 'ALL', all atom types are included as first-in-pair.
        
        Raises: 
            pdffit2.unassignedError if selected phase does not exist
            ValueError if selected atom type does not exist
        """
        import types
        if type(i) in types.StringTypes and i.upper() in self.selalias:
            i = self.selalias[i.upper()]
        pdffit2.isel(self._handle, iset, i)
        return


    def idesel(self, iset, i):
        """idesel(iset, i) --> Do not use atoms of type i from phase iset
        as first in pair distance evaluation.  Used for calculation of
        partial PDF.  When i is 'ALL', all atom types are excluded from
        first-in-pair.
        
        Raises: 
            pdffit2.unassignedError if selected phase does not exist
            ValueError if selected atom type does not exist
        """
        import types
        if type(i) in types.StringTypes and i.upper() in self.selalias:
            i = self.selalias[i.upper()]
        pdffit2.idesel(self._handle, iset, i)
        return


    def jsel(self, iset, i):
        """jsel(iset, i) --> Include atom i from phase iset as second
        in pair distance evaluation.  Used for calculation of partial PDF.
        When i is 'ALL', all atom types are included as second-in-pair.
        
        Raises: 
            pdffit2.unassignedError if selected phase does not exist
            ValueError if selected atom type does not exist
        """
        import types
        if type(i) in types.StringTypes and i.upper() in self.selalias:
            i = self.selalias[i.upper()]
        pdffit2.jsel(self._handle, iset, i)
        return


    def jdesel(self, iset, i):
        """jdesel(iset, i) --> Do not use atoms of type i from phase iset
        as second in pair distance evaluation.  Used for calculation of
        partial PDF.  When i is 'ALL', all atom types are excluded from
        second-in-pair.
        
        Raises: 
            pdffit2.unassignedError if selected phase does not exist
            ValueError if selected atom type does not exist
        """
        import types
        if type(i) in types.StringTypes and i.upper() in self.selalias:
            i = self.selalias[i.upper()]
        pdffit2.jdesel(self._handle, iset, i)
        return


    def bang(self, ia, ja, ka):
        """bang(ia, ja, ka) --> Get the bond angle defined by atoms ia, ja, ka.
        
        Raises: ValueError if selected atom(s) does not exist
                pdffit.unassignedError when no structure has been loaded
        """
        ba = pdffit2.bang(self._handle, ia, ja, ka)
        return ba


    def blen(self, *args):
        """blen(ia, ja) --> Get length of bond defined by atoms ia and ja.  

        blen(a1, a2, lb, ub) --> Print length of all a1-a2 bonds in range
        [lb,ub], where a1 and a2 are integers representing atom types. 1
        represent the first type of atom in the phase, 2 represents the second
        type of atom in the structure, an so on. Either a1 or a2 can be the
        keyword ALL, in which all atom types are used for that end of the
        calculated bonds.
        
        Raises: ValueError if selected atom(s) does not exist
                pdffit.unassignedError when no structure has been loaded
        """
        if len(args)==2:
            res = pdffit2.blen(self._handle, args[0], args[1])
            return res
        elif len(args)==4:
            a1 = args[0]
            a2 = args[1]
            lb = args[2]
            ub = args[3]
            import types
            if type(a1) in types.StringTypes and a1.upper() in self.selalias:
                a1 = self.selalias['ALL']
            if type(a2) in types.StringTypes and a2.upper() in self.selalias:
                a2 = self.selalias['ALL']
            pdffit2.blen(self._handle, a1, a2, lb, ub)
            return
        else: 
            message = "blen() takes 3 or 5 arguments (%i given)" % (len(args)+1)
            raise TypeError, message
        return


    def show_scat(self, stype):
        """show_scat(stype) --> Print scattering length for all atoms.
        
        stype -- 'X' (xray) or 'N' (neutron).
        
        Raises: pdffit2.unassignedError if no phase exists
        """
        pdffit2.show_scat(self._handle, self.Sctp[stype])
        return


    def show_scat_string(self, stype):
        """show_scat_string(stype) --> Get string with scattering length for all
        atoms.
        
        stype -- 'X' (xray) or 'N' (neutron).
        
        Raises: pdffit2.unassignedError if no phase exists
        
        Returns: string containing screen ouput
        """
        return pdffit2.show_scat(self._handle, self.Sctp[stype])


    def set_scat(self, *args):
        """set_scat('N', itype, len) --> Set neutron scattering length for itype
        atoms.  
        
        set_scat('X', a1, b1, a2, b2, a3, b3, a4, b4, c) --> I don't know what
        this does.  
        
        Raises: 
            pdffit2.unassignedError if no phase exists
            ValueError if input variables are bad 
        """
        if len(args) == 3:
            pdffit2.set_scat(self._handle, self.Sctp[args[0]], args[1], args[2])
        elif len(args) == 11:
            pdffit2.set_scat_c(self._handle,self.Sctp[args[0]],args[1],args[2],
              args[3],args[4],args[5],args[6],args[7],args[8],args[9],args[10])
        return


    def reset_scat(self, stype, itype):
        """reset_scat(stype, itype) --> I don't know what this does.
        
        Raises: 
            pdffit2.unassignedError if no phase exists
            ValueError if input variables are bad 
        """
        pdffit2.reset_scat(self._handle, self.Sctp[stype], itype)
        return


    def num_atoms(self):
        """num_atoms() --> Get number of atoms in current phase.
        
        Raises: pdffit2.unassignedError if no atoms exist
        """
        return pdffit2.num_atoms(self._handle)


    # Begin refineable variables.

    def lat(self, n):
        """lat(n) --> Get reference to lattice variable n.
        
        n can be an integer or a string representing the lattice variable.
        1 <==> 'a'
        2 <==> 'b'
        3 <==> 'c'
        4 <==> 'alpha'
        5 <==> 'beta'
        6 <==> 'gamma'
        """
        LatParams = { 'a':1, 'b':2, 'c':3, 'alpha':4, 'beta':5, 'gamma':6 }
        import types
        if type(n) is types.StringType:
            n = LatParams[n]
        return "lat(%i)" % n


    def x(self, i):
        """x(i) --> Get reference to x-value of atom i."""
        return "x(%i)" % i


    def y(self, i):
        """y(i) --> Get reference to y-value of atom i."""
        return "y(%i)" % i


    def z(self, i):
        """z(i) --> Get reference to z-value of atom i."""
        return "z(%i)" % i


    def u11(self, i):
        """u11(i) --> Get reference to U(1,1) for atom i.
        
        U is the anisotropic thermal factor tensor.
        """
        return "u11(%i)" % i


    def u22(self, i):
        """u22(i) --> Get reference to U(2,2) for atom i.
        
        U is the anisotropic thermal factor tensor.
        """
        return "u22(%i)" % i


    def u33(self, i):
        """u33(i) --> Get reference to U(3,3) for atom i.
        
        U is the anisotropic thermal factor tensor.
        """
        return "u33(%i)" % i


    def u12(self, i):
        """u12(i) --> Get reference to U(1,2) for atom i.
        
        U is the anisotropic thermal factor tensor.
        """
        return "u12(%i)" % i


    def u13(self, i):
        """u13(i) --> Get reference to U(1,3) for atom i.
        
        U is the anisotropic thermal factor tensor.
        """
        return "u13(%i)" % i


    def u23(self, i):
        """u23(i) --> Get reference to U(2,3) for atom i.
        
        U is the anisotropic thermal factor tensor.
        """
        return "u23(%i)" % i


    def occ(self, i):
        """occ(i) --> Get reference to occupancy of atom i."""
        return "occ(%i)" % i


    def pscale(self):
        """pscale() --> Get reference to pscale.
       
        pscale is the fraction of the total structure that the current phase
        represents.
        """
        return "pscale"


    def pfrac(self):
        """pfrac() --> same as pscale.
       
        pscale is the fraction of the total structure that the current phase
        represents.
        """
        return self.pscale()


    def srat(self):
        """srat() --> Get reference to sigma ratio.
        
        The sigma ratio determines the reduction in the Debye-Waller factor for
        distances below rcut.
        """
        return "srat"


    def delta(self):
        """delta() --> Get reference to delta.
        
        The phenomenological correlation constant in the Debye-Waller factor.
        The (1/R^2) peak sharpening factor.
        """
        return "delta"


    def gamma(self):
        """gamma() --> Get reference to gamma.
        
        1/R peak sharpening factor.
        """
        return "gamma"


    def dscale(self):
        """dscale() --> Get reference to dscale.
        
        The data scale factor.
        """
        return "dscale"

    def qsig(self):
        """qsig() --> Get reference to qsig.
       
        instrument q-resolution factor.
        """
        return "qsig"


    def qalp(self):
        """qalp() --> Get reference to qalp.
       
        Quadratic peak sharpening factor.
        """
        return "qalp"


    def rcut(self):
        """rcut() --> Get reference to rcut.
        
        rcut is the value of r below which peak sharpening, defined by the sigma
        ratio (srat), applies.
        """
        return "rcut"


    # End refineable variables.

    def __init__(self, data_server=None):
        
        self.data_server = data_server
        self.stru_files = []
        self.data_files = []

        self._handle = pdffit2.create()
        return
    

    def __getRef(self, var_string):
        """Return the actual reference to the variable in the var_string.
        
        This function must be called before trying to actually reference an
        internal variable. See the constrain method for an example.
        
        Raises: 
            pdffit2.unassignedError if variable is not yet assigned
            ValueError if variable index does not exist (e.g. lat(7))
        """
        # people do not use parenthesis in their scripts, e.g., "getvar(qsig)"
        # in such case var_string is a reference to PdfFit method
        import types
        if type(var_string) is types.MethodType:
            var_string = var_string()
        arg_int = None
        try:
            method_string, arg_string = var_string.split("(")
            method_string = method_string.strip()
            arg_int = int(arg_string.strip(")").strip())
        except ValueError: #There is no arg_string
            method_string = var_string.strip()

        f = getattr(pdffit2, method_string)
        if arg_int is None:
            retval = f(self._handle)
            return retval
        else:
            retval = f(self._handle, arg_int)
            return retval

    
    # End of class PdfFit


# version
__id__ = "$Id$"

# End of file
