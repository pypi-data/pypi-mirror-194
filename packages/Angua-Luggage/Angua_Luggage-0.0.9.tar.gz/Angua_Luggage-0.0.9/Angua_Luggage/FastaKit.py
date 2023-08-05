# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 14:10:34 2022

@author: mwodring
"""

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Blast import NCBIXML
from Bio import Entrez

import os
import subprocess
import csv
from shutil import move as shmove

from .utils import new_logger, count_calls, Cleanup

import yaml
from rpy2 import robjects as r

from collections import defaultdict
from .AnguaUtils import back_mapper

import importlib.resources
from . import data

#Angua_test needs changing to Python 3.9+ to use resources.files.
fasta_yaml = importlib.resources.open_binary(data, "fastaTool.yaml")
fastaTool_dict = yaml.full_load(fasta_yaml)

class seqHandler: 
    #Sets up a logger object.
    _logger = new_logger(__name__)
    
    #The seqHandler will store the file and folder names.
    def __init__(self, fasta = "", xml = "", folder = "", folder_type = "misc"):
        self.blast_file = False
        self._folders = {}
        self._pfam_tools = []
        if fasta != "":
            self.addFasta(fasta)
        if xml != "":
            self.blast_file = xml
            self.blast_file_name = "".join(self.blast_file)[-1][:-4]
        if folder != "":
            self.addFolder(folder_type, folder)
    
    #Allows adding a .fasta file to the seqHandler after init.
    #Will also use SeqIO to parse the fasta into an object.
    def addFasta(self, filename: str):
        self.fasta_file = os.path.abspath(filename)
        self.fasta_file_name = self.fasta_file.split("/")[-1][:-6]
        self._seq_object = SeqIO.parse(self.fasta_file, "fasta")
        self._seq_dict = SeqIO.to_dict(SeqIO.parse(self.fasta_file, "fasta"))       
    
    def addRma(self, filename: str, sortby = "contig"):
        self._rma_tool = rmaTool(filename, sortby)
        self._logger.info("Added: " + str(self._rma_tool))
        
    def addFolder(self, folder_type: str, folder: str):
        self._folders[folder_type] = folder
    
    #Generator for a given folder - looks for the file end in the 'pointer' - the name of the folder, so the dict key.
    #Defaults to fetching fasta files from the dict key labelled as contigs, which is the usual.
    def getFiles(self, folder_type = "misc", file_end = ".fasta"):
        for file in os.listdir(self._folders[folder_type]):
            if file.endswith(file_end):
                yield f"{self._folders[folder_type]}/{file}" 
             
    #Runs SRAToolkit on a file outputted by the SRA Run Selector. i.e. one accession per line txt file.
    def fetchSRA(self, output_folder: str, SRA_file: str):
        self.addFolder(folder = output_folder, folder_type = "raw")
        with open(SRA_file, "r") as accessions:
            for accession in accessions.readlines():
                #Trying to move away from FastaKit logging to getting Angua to do it but unsure how to do that here.
                self._logger.info(f"Fetching {accession}")
                #.strip is added due to trailing newlines.
                #https://blog.dalibo.com/2022/09/12/monitoring-python-subprocesses.html
                cmd = ["fasterq-dump", "-p", "-S", "-O", output_folder, accession.strip()]
                with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
                    errs = []
                    for line in proc.stderr:
                        self._logger.info(line.strip())
                        errs.append(line)
                    stdout, _ = proc.communicate()
                #result = subprocess.CompletedProcess(cmd, proc.returncode, stdout, "\n".join(errs))
                for file in self.getFiles(folder_type = "raw", file_end = ".fastq"):
                    subprocess.run(["pigz", "-9", file])
        #In future I would like to find a way for this to check the filesize of the accessions against the memory available.
        
    def renameSRA(self):
        sample_num = 1
        for file in self.getFiles(folder_type = "raw", file_end = "_1.fastq.gz"):
            #I did this in two steps for readability, plus maybe this could be made into a function or whatever along the line.
            #It splits off the filename with extension, then just grabs the filename sans extension, then finally snips off the underscore to just get the SRR--.
            filename = file.split("/")[-1]
            filename_no_extension = filename.split(".")[0]
            samplename = filename_no_extension.split("_")[0]   
            #Uses the fact the SRR reads are stored under the 'raw' folder type in seqHandler. Extension is based on what Angua anticipates.
            new_filename = f"{self._folders['raw']}/{samplename}_S{sample_num}_L001_R1_001.fastq.gz"
            os.rename(file, new_filename)
            #Same for second read. This just ensures the reads get the same sample name. 
            new_filename_R2 = new_filename.replace("R1", "R2")
            file_R2 = file.replace("_1", "_2")
            os.rename(file_R2, new_filename_R2)
            #Last of all increment the sample number.
            sample_num += 1
        #Returns the sample number for logging purposes if so desired.
        return sample_num
                              
    #Creates a fasta file from a list of NCBI accessions.
    #Needs an email, api is optional but allows faster retrieval.
    def fetchEntrezFastas(self, id_list: list, email: str, output: str, api = False, proxy = 3128):
        #To help with FERA proxy shenanigans.
        os.environ["https_proxy"] = f"http://webcache:{proxy}"
        self.fasta_file = f"{output}/viruses.fasta"
        Entrez.email = email
        if api:
            api_key = api
        handle = Entrez.efetch(db = "nucleotide", 
                               id = id_list, 
                               rettype = "fasta")
        sequences = SeqIO.parse(handle, "fasta")
        with open(self.fasta_file, "wt") as fasta_file:
            #SeqIO returns the count when it works, which is handy.
            count = SeqIO.write(sequences, fasta_file, "fasta")
        self._logger.info(f"{count} sequences found and written.")
    
    #Checks if there's a Blast record attached to the seqHandler.
    #If not, it will run a blastx search with the fastas it has attached.
    #NOTE: Amend to also get blastp/n etc if needed. Maybe with a dict of functions.
    def get_BlastRecord(self, search_term: str, minlength: int, get_all: bool):
        if not self.blast_file:
            self.blast_file = self.fasta_file[:-6] + "_blastx.xml"
            self._logger.info("Performing blastx, please wait.")
            subprocess.run("blastx", "-query", self.fasta_file, 
                           "-db", "/nfs/bigbio_00/smcgreig/Blast_databases/nr/nr_db_27012022/nr",
                           "-num_alignments", "5", 
                           "-num_threads", "12", "-outfmt", "5", "-out", self.blast_file)
        #    self._logger.info(f"Blastx generated with {blast_run}")
        #Attaches a blastTool to the seqHandler. It keeps track of the filename and remember the .fasta.
        self._blastTool = blastTool(self.blast_file)
        self._blastTool.getAlignments(search_term, minlength, get_all)
     
    #Generates a fasta tool for each hit in the blast record, using the inputted fasta file.
    #Each fastaTool represents one contig.
    def unpackBlastRecord(self):
        if not self._blastTool:
            self._logger.error("No blast record to unpack.")
            return 
        unpacked_records = self._blastTool.unpackBlastRecord()
        self._fasta_tools = [fastaTool(ID = record[0], frame = record[1], code = self._seq_dict[record[0]].seq) for record in unpacked_records] 
            
    #Makes a blastDB from either a manually inputted fasta file or the one attached to the seqHandler.    
    def makeBlastDb(self, outputdir: str, dbname = "db", fasta_path = ""):
        if fasta_path == "":
            fasta_path = self.fasta_file
        subprocess.run(["makeblastdb", 
                        "-in", fasta_path, 
                        "-dbtype", "nucl", 
                        "-input_type", "fasta", 
                        "-out", f"{outputdir}/{dbname}"])
     
    #Just an override so the seqHandler prints itself when implemented.
    #Tools are not intended to be accessed without seqHandlers.  
    @count_calls
    def outputCSV(self, outputdir: str, filename: str, add_text: str):
        self._blastTool.outputCSV(outputdir, filename, add_text)
        
    #Writes the fastaTools to a new fasta file. For example after TextSearch. 
    @count_calls
    def outputFasta(self, outputdir: str, add_text: str):
        # This list comprehension makes a new SeqRecord (i.e. single fasta entry)
        # for each fastaTool attached to the seqHandler.
        all_fastas = [SeqRecord(seq = tool.code, 
                                id = tool.ID.split(" ")[0], 
                                description = "_".join(tool.ID.split(" ")[1:])) for tool in self._fasta_tools]
        output_file = f"{outputdir}/{self.fasta_file_name}_{add_text}.fasta"
        with open(output_file, "w+") as output_handle:
            SeqIO.write(all_fastas, output_handle, "fasta")
        self._logger.info(output_file + " written.")
        
    def outputFullLog(self, funcs: list):
        func_dict = {"Fastas" : seqHandler.outputFasta,
                     "Alignments" : blastTool.getData,
                     "CSVs" : seqHandler.outputCSV}
        to_log = [f"{func} processed: {func_dict[func].num_calls}" for func in funcs]
        log_string = "\n".join(to_log)
        self._logger.info(log_string)
        
    def rmaToFasta(self, outputdir: str):
        unpacked, sortedby = self._rma_tool.unpackInfo()
        if sortedby == "contig":
            self._fasta_tools = [fastaTool(ID = f"{contig}_{unpacked[contig][1]}", code = self._seq_dict[contig].seq) for contig in unpacked]
            self.outputFasta(outputdir = outputdir, add_text = "_rma_by_contig")
        elif sortedby == "virus":
            for virus in unpacked:
                virus_str = ("_").join(virus.split())
                self._fasta_tools = [fastaTool(ID = f"{contig}_{virus}", code = self._seq_dict[contig].seq) for contig in unpacked[virus]]
                self.outputFasta(outputdir = outputdir, add_text = f"{virus_str}_contigs")
        else:
            self._logger.error("No rma detected.")
            return
    
    @staticmethod
    def splitBbduk(trimmed_dir) -> list:
        for file in os.scandir(trimmed_dir):
            if file.name.endswith("_R1.fastq.gz"):
                filename = "".join(file.name.split(".")[-3])
                R2_file = f"{filename.replace('_R1', '_R2')}.fastq.gz"
                os.mkdir(f"{trimmed_dir}/{filename[:-3]}/")
                shmove(f"{trimmed_dir}/{file.name}", f"{trimmed_dir}/{filename[:-3]}/{file.name}")
                shmove(f"{trimmed_dir}/{R2_file}", f"{trimmed_dir}/{filename[:-3]}/{R2_file}")
    
    @staticmethod        
    #Later seqHandler might be able to integrate the Angua outputs but for now, old fashioned way.
    def backMapToBedGraph(trimmed_dir: str, out_dir: str, ref_file: str):
        just_filename = "".join(ref_file.split("/")[-1])
        ref_sample_name = "_".join(just_filename.split("_")[:2])
        seqHandler.splitBbduk(trimmed_dir)
        for d in os.listdir(trimmed_dir):
            if d == ref_sample_name:
                back_mapper(input_dir = f"{trimmed_dir}/{d}/", output_dir = out_dir, reference = ref_file, threads = 10, delim = "_", mapq = "0", flag = 2304, coverage = "Y", min_alignment_length = 50, softclip_perc = 1.0)  
        if os.path.exists(out_dir):
            #Must bea better pathing.
            for d in os.listdir(out_dir):
                for seq in os.scandir(f"{out_dir}/{d}"):
                    if seq.name.endswith("_sort.bam"):
                        seqname = seq.name[:-4]
                        #https://blog.liang2.tw/posts/2016/01/plot-seq-depth-gviz/#convert-sequencing-depth-to-bedgraph-format
                        os.system(f"bedtools genomecov -bg -ibam {out_dir}/{d}/{seq.name} | gzip > {out_dir}/{d}/{seqname}.bedGraph.gz")
    
    def runPfam(self, db_dir: str, outdirname: str, trimmed_dir: str, add_text = "_Pfam") -> str:
        ORFs, fastas, grl = self.getORFs()
        self.addFolder("pfam", f"{self._folders['contigs']}/{outdirname}")
        outdir = self._folders["pfam"]
        try:
            os.mkdir(outdir)
        except FileExistsError:
            pass
        for subfolder in os.scandir(self._folders["ORFs"]):
            for file in os.listdir(subfolder):
                if file.endswith("aa_.fasta"):
                    fasta_filename = file.split("/")[-1][:-14]
                    outfile = f"{outdir}/{fasta_filename}{add_text}.json"
                    self._pfam_tools.append(pfamTool(fasta_file = f"{self._folders['ORFs']}/{subfolder.name}/{file}", 
                                                     db_dir = db_dir, outfile = outfile))
       
        pfam_output = r.r['loop_json_files'](self._folders["pfam"], ORFs)
        pfam_grl = pfam_output.rx2("pfam")
        pfam_df = pfam_output.rx2("df")
        
        for fasta in fastas:
            fasta_name = os.path.basename(fasta)[:-6]
            #sample_name = "".join(fasta_name.split("_")[6:])
            seqHandler.backMapToBedGraph(trimmed_dir, f"{self._folders['contigs']}/{outdirname}/backmap/{fasta_name}", f"{self._folders['contigs']}/{fasta_name}.fasta")
        
        Cleanup([self._folders["contigs"]],[".64", ".pac", ".fai", ".ann", ".amb", ".0123"])
        r.r['generate_orf_plots'](grl, self._folders["contigs"], fastas, f"{self._folders['contigs']}/ORF_plots", pfam_grl, pfam_df, f"{self._folders['contigs']}/{outdirname}/backmap/")
        
    
    def getORFs(self):
        r_script = importlib.resources.open_binary(data, 'orfs.r')
        r.r.source(r_script)
        
        ORF_output = r.r['loop_fasta_files'](self._folders["contigs"], "Virus_ORFs", 150)
        self.addFolder("ORFs", f"{self._folders['contigs']}/Virus_ORFs")
        log = ORF_output.rx2("log")
        ORFs = ORF_output.rx2("ORFs")
        fastas = ORF_output.rx2("files")
        grl = ORF_output.rx2("grl")
        
        for i, _ in enumerate(log):
            self._logger.info(log.rx2(i+1))
        return ORFs, fastas, grl
        
class pfamTool(seqHandler):
    def __init__(self, fasta_file, db_dir, outfile):
        with open(outfile, "w") as output:
            subprocess.run(["pfam_scan.pl", "-fasta", fasta_file, "-dir", db_dir, "-json", "pretty"], stdout = output)
        self._json = outfile
    
class fastaTool(seqHandler):
    __slots__ = ['code', 'frame', 'codedict', 'ID', "transl_protein"]
      
    #I have to do this to make sure it's ordered.
    dict_tuple = (fastaTool_dict["degeneratedna"], 
                  fastaTool_dict["aminoacids"], 
                  fastaTool_dict["degenerateacids"], 
                  fastaTool_dict["complimentarityDNA"],
                  fastaTool_dict["complimentarityRNA"], 
                  fastaTool_dict["standard_codons"])
    degeneratedna, aminoacids, degenerateacids, complimentarityDNA, complimentarityRNA, standard_codons = dict_tuple
    
    #Simple function to get the degeneracy of a given oligo. 
    def countDegeneracy(oligo):
        multiply_list = [len(fastaTool.degeneratedna[letter]) for letter in oligo if letter in fastaTool.degeneratedna]
        result = 1
        for number in multiply_list:
            result = result * number
        return result      

    #Generates a set of all possible oligos for a degenerate primer, for use with Blast and so on.
    def findDegeneratePrimers(oligo):
      #Converts the primer into a graph of possible paths through the options.
      graph, end_node_num = fastaTool.degenOligoToGraph(oligo)
      #Previous function appends a number to the strings. It's a list because sometimes the first nucleotide is degenerate.
      start_nodes = [node for node in graph if node.endswith("0")]
      #If the last letter is a 'normal' nucleotide, this just makes sure it adds the last nucleotides on, otherwise it will stop at the last degenerate nucleotide.
      if oligo[-1] in ["A", "G", "T", "C"]:
          end_node_num += 1
      #Finds the end nodes.
      end_nodes = [oligo for edge in graph.values() for oligo in edge if oligo.endswith(str(end_node_num))]
      all_paths = []
      all_oligo_lists = []
      #The below goes from start to end for all possible start-end combos.
      for start in start_nodes:
          for end in end_nodes:
              all_paths.append(fastaTool.find_all_paths(graph, start, end))
      for start_end_combo in all_paths:
          #Nested because a start-end combination will have multiple possible paths through it. In theory this can just be one start, but there will usually be multiple ends.
          for path in start_end_combo:
              full_oligo = []
              for seq in path:
                  #Remove the number used to keep the graph in order.
                  #https://www.studytonight.com/python-howtos/remove-numbers-from-string-in-python
                  new_seq = ''.join(filter(lambda x: not x.isdigit(), seq))
                  #Build out the oligo.
                  full_oligo.append(new_seq)
              #Adds the full oligo (which is presently a list of nucleotides) to a running list of all possible options.
              all_oligo_lists.append(full_oligo)
      #Set to prevent duplicates. I might be able to refactor so it doesn't produce duplicates in future.
      all_oligos = set()
      for oligo_list in all_oligo_lists:
          #Convert the list of nucleotides to a string and create a list of possible strings. 
          oligo = "".join(oligo_list)
          all_oligos.add(oligo)
      return all_oligos
      
    #Generates a graph representing a path through the potential options in a degenerate oligo.
    def degenOligoToGraph(oligo):
        #Turns it into a list in case a string was inputted.
        oligo_list = [letter for letter in oligo]
        
        #Instantiate lists and incremented ints.
        current_string = []
        present_nodes = []
        #-1 so it increments to 0, thus matching the indexing on the lists it interacts with.
        current_node_num = -1
        graph = {}
        
        for i, letter in enumerate(oligo_list):
            #Checks if it's just a regular base.
            if letter in ["A", "G", "C", "T"]:
                #Builds a list that represents a sequence of non-polymorphic nucleotide letters.
                current_string.append(letter)
                #This is in case the last letter is a normal base.
                if i == len(oligo_list) - 1:
                    #If it's after a branch.
                    if len(present_nodes) > 0:
                        for node in present_nodes:
                            node = node + str(current_node_num)
                            graph.setdefault(node, [])
                            graph[node].append("".join(current_string) + str(current_node_num + 1))
                    else:
                        graph["".join(current_string, str(current_node_num + 1))] = []
            elif letter in fastaTool.degeneratedna:
                #present_nodes represents the node we're accessing. It's a list because each branch can be polymorphic in itself.
                if len(present_nodes) > 0:
                    for node in present_nodes:
                        #Appends a number so identical sequences don't get assembled into nonsense or cyclic oligos.
                        node = node + str(current_node_num)
                        graph.setdefault(node, [])
                        #Builds the edges using the possible branches THESE branches connect to.
                        for base in fastaTool.degeneratedna[letter]:
                            current_string.append(base)
                            graph[node].append("".join(current_string) + str(current_node_num + 1))
                            current_string.pop()
                    present_nodes = []
                #Builds the next node ready to be used - the first runthrough will just build the starting node, since it skips the above 'if'.
                for base in fastaTool.degeneratedna[letter]:
                    current_string.append(base)
                    present_nodes.append("".join(current_string))
                    current_string.pop()
                #Increments the ID number.
                current_node_num += 1
                current_string = []
        return graph, current_node_num
    
    #Adapted from https://www.python.org/doc/essays/graphs/.
    def find_all_paths(graph, start, end, path = 0):
        #First runthrough will instantiate the list, since you can't pass empty lists as defaults.
        if path == 0:
            path = []
        #Adds the start to the empty list. Note that because this is recursive, the start won't be the beginning - just where this iteration starts.
        path = path + [start]
        #Checks if we reached the desired end.
        if start == end:
            return [path]
        #Fails out if for some reason the start is nonsense.
        if not start in graph:
            return []
        paths = []
        #Goes through connecting nodes from the desired start.
        for node in graph[start]:
            #Checks it isn't going in circles.
            if node not in path:
                #Recursively calls with this node as the start.
                newpaths = fastaTool.find_all_paths(graph, node, end, path)
                #Once it finds all possible paths, drops them into a list like so.
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
     
    #Checks what type of code is attached to the fastaTool.
    def validateType(self, code: str) -> dict:
        #Honestly forget why I need to do this but you do.
        code = code.join(code.split())
        #Defaults to DNA.
        codedict = fastaTool.complimentarityDNA
        DNAletters = ("G", "C", "A", "T")
        Tcount = 0
        for letter in code.upper():
            if letter == "T":
                Tcount += 1
            if letter not in DNAletters:
                #Returns RNA if there's Us but no Ts.
                if letter == "U" and not Tcount == 0:
                    codedict = self.complimentarityRNA
                    continue
                #Returns amino acid if the letter isn't RNA/DNA but IS amino acid.
                elif letter in self.aminoacids.keys():
                    codedict = self.standard_codons
                    continue
                #Returns none if the inputted code is gibberish.
                else:
                    codedict = "None"
                    self._logger.error("Code type not valid.")
        return codedict
    
    def NucleotideCount(self) -> int:
        Acount = self.code.count("A")
        Tcount = self.code.count("T")
        Gcount = self.code.count("G")
        Ccount = self.code.count("C")
        return Acount, Tcount, Gcount, Ccount
    
    @staticmethod
    def transcribeDNA(DNA: str) -> str:
        output = ("U" if letter == "T" else letter for letter in DNA)
        return "".join(output)
    
    @staticmethod
    def reverseComplement(code: str, codetype: dict) -> str:
        complement_letters = [codetype[letter] for letter in list(code)]
        complement_letters.reverse()
        return "".join(complement_letters)
        
    def translateNuc(self) -> SeqRecord:
        code = self.code
        frame = self.frame
        #This function relies on Blastx to work out the frame.
        if frame == "N/A":
            self._logger.error(f"{self.ID} has no frame value - suggest manual alignment.")
            return
        #Checks if the contig is backwards.
        if frame < 0:
            code = self.reverseComplement(code, self.codedict)
            frame = abs(frame)
        #Translates in frame.
        if self.codedict == self.complimentarityDNA:
            code = self.transcribeDNA(code)
        #No point translating amino acids...
        if self.codedict == fastaTool.aminoacids:
            self._logger.error("Can't translate peptides!")
            return
        
        #Makes a list, then fills it with amino acids from codons as it moves along.
        protein_letters = []
        start = frame - 1
        end = start + 3
        while start <= (len(code) - 3):
            codon = code[start:end]
            protein_letters.append(fastaTool.standard_codons[codon])
            start += 3
            end += 3
        #List to string.
        self.transl_protein = "".join(protein_letters)
        #Returns a SeqRecord of the protein with the same name as the original DNA.
        return SeqRecord(self.transl_protein, self.ID)
    
    #Slices a fasta into chunks of given size - first x or last x.
    def sliceFasta(fasta: SeqRecord, length: int, last = False):
        new_fasta = []
        for seq in fasta:
            #Doesn't slice it if it's shorter than the intended size.
            if length > len(seq): length = len(seq) - 1
            sliced = seq.seq[length:] if last else seq.seq[:length]
            new_seq = SeqRecord(sliced, seq.id)
            new_fasta.append(new_seq)
        SeqIO.write(new_fasta, f"{fasta[:-6]}_sliced.fasta", "fasta")

    def __init__(self, code: str, frame = 1, ID = "N/A"):
        self.ID = ID
        self.codedict = self.validateType(code)
        self.code = code
        self.frame = frame

class blastTool(seqHandler):
    #Header for outputted .csvs. The order is relevant so don't juggle it
    #just attach to the end.
    header = ("species", "query % coverage", 
              "% identity", "contig length", 
              "contig name", "NCBI accession", 
              "BLAST score", "Frame", "alignment", 
              "matched length")
    __slots__ = ['filename', 'queries', 'blast_type', 'aln', 'query_count']
    
    def __init__(self, handle: str):
        self.filename = handle.split("/")[-1][:-4]
        result_handle = open(handle)
        self.queries = NCBIXML.parse(result_handle)
        self.blast_type = "None"
        self.aln = {}
        self.query_count = 0
        
    def __str__(self):
        return f"{self.filename} : {len(self.aln)} hits over {self.query_count} contigs greater than minimum length bp."
    
    def unpackBlastRecord(self) -> list:
        records = []
        for hit in self.aln.values():
            contig_name = hit["contig name"]
            if contig_name == "":
                self._logger.warning(f"No alignment found for {hit}.")
                continue
            contig_id = contig_name.split(" ")[0]
            current_fasta = [contig_id, hit["Frame"]]
            records.append(current_fasta)
        return records
                        
    
    def getAlignments(self, search_term: str, minlength: int, get_all = False):
        for query in self.queries:
            #Fetches the application type if it doesn't already know.
            if self.blast_type == "None":
                self.blast_type = query.application
            if len(query.alignments) == 0 or query.query_length < minlength:
                continue
            self.query_count += 1
            to_check = len(query.alignments) if get_all == True else 1
            for i in range(to_check):
                alignment = query.alignments[i]
                #Checks if there is a search term, and if that term is in the hit.
                if search_term and search_term not in alignment.hit_def.upper():
                    continue
                #Appends alignment to the aln dict. q1a1 = query 1, alignment 1.
                self.aln[f"q{self.query_count}a{i+1}"] = self.getData(alignment, query)
                
    @count_calls            
    def getData(self, alignment, query, hspno = 0) -> dict:
        def getpercentage(a, b):
            return(a / b) * 100
        #Assumes no frame.
        frame = "N.A"
        hsp = alignment.hsps[hspno]
        ungapped = hsp.align_length - hsp.gaps
        coverage = getpercentage(ungapped,
                                 query.query_length)
        identity = getpercentage(hsp.identities, 
                                 hsp.align_length)
        
        #These go by the formatting outputted by NCBI - 
        #the accession number is in the ID at different places.
        if self.blast_type.endswith("N"):
            splitnum = 3
        elif self.blast_type.endswith("P"):
            splitnum = 1
        elif self.blast_type.endswith("X"):
            splitnum = 1
            #Adds the frame back in if it's a Blastx.
            frame = hsp.frame
            
        accession = alignment.hit_id.split("|")[splitnum]  
        db_type = alignment.hit_id.split("|")[0]
        #Unused for now - gb is genbank, ref is refseq.
        
        #Must be in the same order as the header.
        dict_values = (alignment.hit_def, 
                       coverage, 
                       identity, 
                       query.query_length, query.query, 
                       accession, hsp.score, 
                       frame[0], hsp.query, ungapped)
        return {title : dict_values[i] for i, title in enumerate(blastTool.header)}
    
    #Outputs a csv with the header and the values.
    def outputCSV(self, output: str, filename: str, add_text: str):
        out_file = f"{output}/{filename}_{add_text}.csv"
        with open(out_file,'w+', encoding='UTF8', newline='') as virus_csv:
            csv_writer = csv.writer(virus_csv)
            csv_writer.writerow(blastTool.header)  
            for hit in self.aln.values():
                csv_writer.writerow(hit.values())    
            self._logger.info(f"csv written to {out_file}.")
    
class rmaTool():
    def __str__(self):
        outputstr = ""
        for key in self._info_dict:
            if self._sorted == "contig":
                outputstr += f"\n {key} : Rank: {self._info_dict[key][0]} Assignment: {self._info_dict[key][1]}"
            elif self._sorted == "virus":
                outputstr += f"\n {key} : {self._info_dict[key]}"
            else:
                outputstr = "Unsorted, quitting."
                break
        return outputstr
    
    #Amend to also run the root.
    @staticmethod
    def runRma2info(filename: str, addtxt = "_info") -> str:
        file_no_extension = filename[:-5]
        #Note: probably worth changing this to all output to a given directory. At the moment it drops it into the MEGAN directory for you.
        outfile = f"{file_no_extension}{addtxt}.txt"
        with open(outfile, "w") as output:
            subprocess.run(["rma2info", "--in", filename, "-vo", "-n", "-r2c", "Taxonomy", "-r"], stdout = output)
        return outfile

    def __init__(self, filename: str, sortby: str):
        funcdict = {"contig" : self.sortByContig,
                    "virus" : self.sortByVirus}
        self.rma_txt = self.runRma2info(filename) if filename.endswith(".rma6") else filename
        self._info_dict = funcdict[sortby]()
    
    def unpackInfo(self):
        return self._info_dict, self._sorted
    
    def sortByContig(self) -> dict:
        info_dict = {}
        with open(self.rma_txt, 'r') as info:
            for line in info.readlines():
                contig_name, rank, *virus_name = line.split("\t")
                virus_name = "_".join(virus_name).strip()
                virus_name = virus_name.replace(" ", "_")
                info_dict[contig_name] = [rank, virus_name]
                print(info_dict[contig_name])
                self._sorted = "contig"
        return info_dict
    
    def sortByVirus(self) -> dict:
        info_dict = defaultdict(list)
        with open(self.rma_txt, 'r') as info:
            for line in info.readlines():
                contig_name, rank, virus_name = line.split("\t")
                virus_name = virus_name.replace(" ", "_")
                info_dict[virus_name].append(contig_name)
        self._sorted = "virus"
        return info_dict
